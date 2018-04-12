""" Create New Settings Wizard 'GARUDA - Sharp | Swift | Strong'

Visual Inspection of Mechanical Components on the Assembly Line using Computer Vision
Author: R Mukesh, IIITDM Kancheepuram
"""

# import necessary libraries needed for GUI creation
from PyQt5.QtWidgets import QApplication, QWidget, QRubberBand
from  PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QTimer, QPoint, QSize, QRect, Qt

import sys

# Import libraries for image display and processing
import cv2 as cv

# import support libraries
from queue import Queue
from threading import Thread, Lock

import time

# Create a custom widget that displays images
class imageViewer(QWidget):

	def __init__(self, parent=None):

		# Initialse and display the QWidget
		super().__init__(parent)
		self.image = None
		self.show()

	# Set an OpenCV image 'frame' on the widget by repainting it
	def setImage(self, frame):

		self.cv_image = frame
		img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

		img_height, img_width, img_nchannels = img.shape
		img_linelength = img_nchannels * img_width

		image = QImage(img.data, img_width, img_height, img_linelength, QImage.Format_RGB888)

		self.image = image
		self.resize(image.size())
		self.update()

	def getImage(self):
		return self.image


	# Override the Paint Event of the widget
	def paintEvent(self, event):

		image_painter = QPainter()
		image_painter.begin(self)

		if self.image:
			image_painter.drawImage(QPoint(0, 0), self.image)
		
		image_painter.end()

# Create a custom widget that captures and displays live video feeds
class cameraFeedWidget(QWidget):

	def __init__(self, parent=None):

		# Initialse and display the QWidget with a image viewer
		super().__init__(parent)
		self.image_viewer = imageViewer(self)
		self.show()

		# Queue to enqueue live camera feed frames
		self.frames_queue = Queue()

		# Indicator variable that teels if feed is RUNNING
		self.running = False

		# variables to select a region of the image (ROI selection)
		self.allow_select_roi = False
		self.select_band = QRubberBand(QRubberBand.Rectangle, self)
		self.select_origin = QPoint(0, 0)
		self.select_band.setGeometry(QRect(self.select_origin, QSize(-1,-1)))

	def enableSelectROI(self):
		self.allow_select_roi = True

	# Start selecting ROI
	def mousePressEvent(self, event):

		if self.allow_select_roi and event.button() == Qt.LeftButton:
		
			self.select_origin = QPoint(event.pos())
			self.select_band.setGeometry(QRect(self.select_origin, QSize()))
			self.select_band.show()

	# Expanding the ROI by dragging the mouse
	def mouseMoveEvent(self, event):

		if self.allow_select_roi:
			self.select_band.setGeometry(QRect(self.select_origin,event.pos()).normalized())

	def startVideoFeed(self, video_source, roi=None):

		self.running = True

		# Start Queuing Frames as a seperate thread
		self.capture_thread = Thread(target=self.queueFrames, args = (video_source, roi))
		self.capture_thread.start()
	
		# Create and start timer that updates frames periodically (every 1 ms)
		self.frame_update_timer = QTimer(self)
		self.frame_update_timer.timeout.connect(self.updateFrames)
		self.frame_update_timer.start(1)

		print("Started Capture and Update Threads ...")


	# Real-time queuing of live video frames
	def queueFrames(self, video_source, roi=None):

		video_feed = cv.VideoCapture(video_source)
		# May optionally modify image properties here - HEIGHT, WIDTH, FPS
		
		while self.running:

			# Grab frames from Video Feed and enqueue
			video_feed.grab()
			read, image = video_feed.retrieve(0)

			if roi:
				image = image[roi[0][0]:roi[1][0]+1, roi[0][1]:roi[1][1]+1]

			if self.frames_queue.qsize() < 10:
				self.frames_queue.put(image)
				# print("Queueing Frames ...")

		# Release the video capture
		video_feed.release()
		print("Video Feed Released")

	def updateFrames(self):
		
		if not self.frames_queue.empty():

			# print("Updating Frames ...")

			# Read the image frame from queue and display
			frame = self.frames_queue.get()
			self.resize(QSize(frame.shape[1], frame.shape[0]))
			self.image_viewer.setImage(frame)
		
	def stopVideoFeed(self):

		# Setting running=False stops the queuing threads
		self.running = False

		# Stop Update (Timer based) threads
		if hasattr(self, 'frame_update_timer'):
			self.frame_update_timer.stop()

		if hasattr(self, 'capture_thread'):
			self.capture_thread.join()


	def closeEvent(self, event):

		# Stop Queuing Thread
		self.running = False

	def captureFrame(self):
		return self.image_viewer.getImage()

# Test the 'Create New Settings Wizard'
if __name__ == '__main__':

	# Create and display the application's 'Create New Settings' wizard
	application = QApplication(sys.argv)
	# window = newSettings_roi_window()
	# window.show()

	# img = cv.imread('scrap/part3.png', cv.IMREAD_COLOR)

	# img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
	# img_height, img_width, img_nchannels = img.shape
	# img_linelength = img_nchannels * img_width
	# image = QImage(img.data, img_width, img_height, img_linelength, QImage.Format_RGB888)

	window = cameraFeedWidget()
	# window.setImage(image)
	window.startVideoFeed(0)

	sys.exit(application.exec_())