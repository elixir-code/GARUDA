""" 'Add components' wizard of application 'GARUDA - Sharp | Swift | Strong'

Visual Inspection of Mechanical Components on the Assembly Line using Computer Vision
Author: R Mukesh, IIITDM Kancheepuram
"""

# import all necessary libraries for GUI creation
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QGroupBox, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

# import related windows
from widget_image import cameraFeedWidget, imageViewer

# import support libraries
import sys
import pickle

# import libraries necessary for feature extraction (Equal Sector Area Shape Descriptor)
sys.path.append('../sources/')
from preprocess_contour import preprocess_image, gen_shape_descriptor

class train_components_window(QWidget):

	def __init__(self, setting_name, url, camera_feed_roi):

		print(url, camera_feed_roi)

		# Initialise the QWidget
		super().__init__()

		# Customise the QWidget
		self.initUI(url, camera_feed_roi)
		self.settings = {'ROI':camera_feed_roi, 'Products':{}}

		self.setting_name = setting_name

	def initUI(self, url, camera_feed_roi):

		# Create and display widgets for Live Camera Feed URL
		camera_url_box = QHBoxLayout()

		camera_url_label = QLabel('Live Camera URL : ')
		
		camera_url_edit = QLineEdit()
		camera_url_edit.setText(str(url))
		camera_url_edit.setEnabled(False)

		camera_capture_btn = QPushButton('Capture')
		camera_capture_btn.setEnabled(False)

		camera_url_box.addWidget(camera_url_label)
		camera_url_box.addWidget(camera_url_edit)
		camera_url_box.addWidget(camera_capture_btn)


		# create and display widgets to read new component name
		component_name_box = QHBoxLayout()
		
		self.new_component_btn = QPushButton(QIcon('icons/plus.png'), None)
		self.new_component_btn.setIconSize(QSize(25, 25))

		self.component_name_edit = QLineEdit()
		self.component_name_edit.setPlaceholderText('Component Name')
		self.component_name_edit.hide()

		component_name_box.addWidget(self.new_component_btn)
		component_name_box.addWidget(self.component_name_edit)

		self.add_component_btn = QPushButton('Add Component')
		self.add_component_btn.setEnabled(False)

		# create and display widgets to display camera feed ROI
		camera_feed_box = QHBoxLayout()

		camera_feed_box.addStretch(1)
		self.camera_feed_viewer = cameraFeedWidget()
		self.camera_feed_viewer.startVideoFeed(url, roi=camera_feed_roi)

		camera_feed_box.addWidget(self.camera_feed_viewer)
		camera_feed_box.addStretch(20)

		# create and display widgets to add new component
		new_component_box = QVBoxLayout()
		
		self.new_component_label = QLabel('To add New Component, Press (+) button')
		self.new_component_label.setStyleSheet('color: green')

		new_component_box.addWidget(self.new_component_label)
		new_component_box.addLayout(component_name_box)
		
		new_component_box.addStretch(1)
		new_component_box.addLayout(camera_feed_box)
		new_component_box.addStretch(50)
		
		new_component_box.addWidget(self.add_component_btn)


		# create and display widgets to display trained components
		trained_comp_scroll = QScrollArea()
		scroll_inner_widget = QWidget()
		
		trained_comp_scroll.setWidget(scroll_inner_widget)
		trained_comp_scroll.setWidgetResizable(True)

		self.trained_scroll_box = QVBoxLayout(scroll_inner_widget)
		scroll_inner_widget.setLayout(self.trained_scroll_box)

		# create and display widgets to add components and display added components
		add_display_comp_box = QHBoxLayout()

		add_display_comp_box.addWidget(trained_comp_scroll)
		add_display_comp_box.addLayout(new_component_box)

		# create and display widgets for 'NEXT' button
		finish_btn_box = QHBoxLayout()
		finish_btn = QPushButton('Finish')

		finish_btn_box.addStretch(1)
		finish_btn_box.addWidget(finish_btn)

		# create and display the main window widgets
		main_box = QVBoxLayout()

		main_box.addLayout(camera_url_box)
		main_box.addLayout(add_display_comp_box)
		main_box.addLayout(finish_btn_box)

		self.setLayout(main_box)

		# Set the attributes of the train components window and display
		self.setGeometry(100, 100, 1000, 620)
		self.setWindowTitle('Create New Settings Wizard - Add Components')
		# self.show()

		# Add Pressed Event Handlers for 'Plus','Add Component' and 'Finish' buttons
		self.new_component_btn.pressed.connect(self.plusPressed)
		self.add_component_btn.pressed.connect(self.addComponentPressed)
		finish_btn.pressed.connect(self.finishPressed)

	# 'Plus' pressed to create new component
	def plusPressed(self):
		
		self.component_name_edit.show()
		self.new_component_label.setText('Place a component under the camera, Enter it\'s Name\nPress \'Add Component\'')
		self.new_component_label.setStyleSheet('color: red')
		self.add_component_btn.setEnabled(True)


	# 'Add Component' pressed to extract features and add a new component
	def addComponentPressed(self):

		component_name = self.component_name_edit.text()

		if component_name == '':
			QMessageBox.warning(self, 'Invalid Product Name', '<b>Empty product names are not allowed</b>. Please enter a product name.', QMessageBox.Ok)
			return


		if component_name in self.settings['Products']:
			QMessageBox.warning(self, 'Invalid Product Name', 'The <b>product name is already in use</b>. Please choose another product name.', QMessageBox.Ok)
			self.component_name_edit.setText('')
			return

		component_image = self.camera_feed_viewer.image_viewer.cv_image

		self.settings['Products'][component_name] = gen_shape_descriptor(preprocess_image(component_image), 10)

		# Display details of newly added component
		new_component_pane = QGroupBox(component_name)
		new_component_box = QVBoxLayout()
		
		new_component_imageViewer = imageViewer()
		new_component_imageViewer.setImage(component_image)
		
		new_comp_feature_label = QLabel(self.settings['Products'][component_name].tolist().__repr__())

		new_component_box.addWidget(new_component_imageViewer)
		new_component_imageViewer.setMinimumSize(new_component_imageViewer.image.size())
		new_component_box.addWidget(new_comp_feature_label)

		new_component_pane.setLayout(new_component_box)
		
		# new_component_pane.setMinimumSize(new_component_imageViewer.size())
		
		self.trained_scroll_box.addWidget(new_component_pane)

		self.component_name_edit.setText('')
		self.component_name_edit.hide()

		self.new_component_label.setText('To add New Component, Press (+) button')
		self.new_component_label.setStyleSheet('color: green')

		self.add_component_btn.setEnabled(False)

		# Generate component model feature and add to settings


	def finishPressed(self):
		# generate and write settings to file
		setting_file = open('../.settings/'+self.setting_name+'.settings', 'xb')
		pickle.dump(self.settings, setting_file)

		QMessageBox.information(self, 'New Settings Created', 'The new setting <b>\'{}\'</b> was sucessfully created'.format(self.setting_name))

		self.close()

	def closeEvent(self, event):
		# Stop the live camera feed
		self.camera_feed_viewer.stopVideoFeed()


# Test the 'Add Component' wizard
if __name__ == '__main__':

	# Create and display the application's 'Add Component' wizard
	application = QApplication(sys.argv)
	
	window = train_components_window('coupler', 0, ((15, 251),(348, 519)))
	window.show()
	# window = train_components_window(0, ((15, 500),(348, 600)))

	sys.exit(application.exec_())
