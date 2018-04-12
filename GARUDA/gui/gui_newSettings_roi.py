""" 'Fix Region of Interest (ROI)' wizard of application 'GARUDA - Sharp | Swift | Strong'

Visual Inspection of Mechanical Components on the Assembly Line using Computer Vision
Author: R Mukesh, IIITDM Kancheepuram
"""

# Import necessary libraries for GUI creation
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox
from PyQt5.QtCore import QSize
from widget_image import cameraFeedWidget
import sys

# import related windows
from gui_newSettings_train import train_components_window

# Customise the QWidget widget to create 'Fix ROI' window
class fix_roi_window(QWidget):

	def __init__(self, setting_name):

		# Initialise the QWidget
		super().__init__()

		# Customise the QWidget
		self.initUI()

		# Initialise ROI of live camera feed
		self.roi_point1 = (None, None)
		self.roi_point2 = (None, None)

		self.camera_feed_url = None
		self.setting_name = setting_name

	def initUI(self):

		# Create and display widgets to read Live Camera Feed URL
		camera_url_box = QHBoxLayout()

		camera_url_label = QLabel('Live Camera URL : ')
		self.camera_url_edit = QLineEdit()
		self.camera_capture_btn = QPushButton('Capture')

		camera_url_box.addWidget(camera_url_label)
		camera_url_box.addWidget(self.camera_url_edit)
		camera_url_box.addWidget(self.camera_capture_btn)

		# create and display widgets to Fix ROI
		fix_roi_box = QVBoxLayout()

		self.fix_roi_label = QLabel('Drag your mouse over the camera feed \nto select your \'Region of Interest\'(ROI)')
		self.fix_roi_label.setStyleSheet('color: red')
		self.fix_roi_btn = QPushButton('Fix ROI')
		self.fix_roi_btn.setEnabled(False)

		roi_region_pane = QGroupBox('ROI Region')
		roi_region_box = QVBoxLayout()

		self.roi_regionp1_label = QLabel('x:{0}, y:{1}'.format(None, None))
		self.roi_regionp2_label = QLabel('x:{0}, y:{1}'.format(None, None))

		roi_region_box.addWidget(self.roi_regionp1_label)
		roi_region_box.addWidget(self.roi_regionp2_label)

		roi_region_pane.setLayout(roi_region_box)

		fix_roi_box.addWidget(self.fix_roi_label)

		fix_roi_box.addWidget(roi_region_pane)
		fix_roi_box.addWidget(self.fix_roi_btn)

		# create and display widgets to display live Camera Feed and fix ROI
		camera_roi_box = QHBoxLayout()

		camera_roi_box.addStretch(1)
		self.camera_feed_viewer = cameraFeedWidget()
		camera_roi_box.addWidget(self.camera_feed_viewer)
		camera_roi_box.addStretch(50)

		camera_roi_box.addStretch(1)
		camera_roi_box.addLayout(fix_roi_box)
		camera_roi_box.addStretch(1)
		
		# Create and display next button
		next_btn_box = QHBoxLayout()
		self.next_btn = QPushButton('Next')
		self.next_btn.setEnabled(False)

		next_btn_box.addStretch()
		next_btn_box.addWidget(self.next_btn)

		# Create and display widgets to display camera feed and fix ROI
		main_box = QVBoxLayout()

		main_box.addLayout(camera_url_box)
		main_box.addStretch(1)
		main_box.addLayout(camera_roi_box)
		main_box.addStretch(20)
		main_box.addLayout(next_btn_box)
		
		self.setLayout(main_box)

		
		# Start capture when 'CAPTURE' pressed
		self.camera_capture_btn.pressed.connect(self.startCapture)

		# Action to take when Fix Button is pressed
		self.fix_roi_btn.pressed.connect(self.fixROIPressed)

		# Action to take when 'Next' button pressed
		self.next_btn.pressed.connect(self.nextPressed)

		# Set the attributes of the fix roi window and display
		self.setGeometry(100, 100, 1000, 600)
		self.setWindowTitle('Create New Settings Wizard - Fix ROI')
		# self.show()

	def startCapture(self):

		self.camera_feed_url = self.camera_url_edit.text()

		if self.camera_feed_url.isdecimal():
			self.camera_feed_url = int(self.camera_feed_url)

		self.camera_feed_viewer.startVideoFeed(self.camera_feed_url)
		self.camera_url_edit.setEnabled(False)
		self.camera_capture_btn.setEnabled(False)
		self.fix_roi_btn.setEnabled(True)

		self.camera_feed_viewer.enableSelectROI()

	def fixROIPressed(self):

		self.roi_point1 = (None, None)
		self.roi_point2 = (None, None)

		# if ROI selection is not empty
		if not self.camera_feed_viewer.select_band.size().isEmpty():

			roi_qpoint1 = self.camera_feed_viewer.select_band.geometry().topLeft()
			self.roi_point1 = (roi_qpoint1.y(), roi_qpoint1.x())
			
			roi_qpoint2 = self.camera_feed_viewer.select_band.geometry().bottomRight()
			self.roi_point2 = (roi_qpoint2.y(), roi_qpoint2.x())

			self.next_btn.setEnabled(True)

		else:
			self.next_btn.setEnabled(False)

		self.roi_regionp1_label.setText("x:{0}, y:{1}".format(*self.roi_point1))
		self.roi_regionp2_label.setText("x:{0}, y:{1}".format(*self.roi_point2))

	# When the next button is pressed
	def nextPressed(self):
		
		self.camera_feed_viewer.stopVideoFeed()

		self.close()
		
		self.train_component_wizard = train_components_window(self.setting_name, self.camera_feed_url, (self.roi_point1, self.roi_point2))
		self.train_component_wizard.show()

	def getROI(self):
		return self.roi_point1, self.roi_point2

	def getCameraURL(self):
		return self.camera_feed_url

	def closeEvent(self, event):

		# Stop the live camera feed
		self.camera_feed_viewer.stopVideoFeed()


# Test the 'Fix ROI' wizard
if __name__ == '__main__':

	# Create and display the application's 'Fix ROI' wizard
	application = QApplication(sys.argv)
	
	window = fix_roi_window()
	window.show()
	
	sys.exit(application.exec_())

