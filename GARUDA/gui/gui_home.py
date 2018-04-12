""" Home Page of application 'GARUDA - Sharp | Swift | Strong'

Visual Inspection of Mechanical Components on the Assembly Line using Computer Vision
Author: R Mukesh, IIITDM Kancheepuram
"""

# Import necessary libraries for GUI creation
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QAction, QToolBar, QHBoxLayout, QVBoxLayout, QInputDialog, QMessageBox, QWidget, QLabel, QGroupBox, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QDateTime, QTimer

from widget_image import cameraFeedWidget

# import related windows
from gui_newSettings_roi import fix_roi_window

# import support libraries
import os
import sys
import pickle

sys.path.append('../sources/')
from preprocess_contour import preprocess_image, gen_shape_descriptor, correlation_coeff

# Customise the QMainWindow widget to create home window
class home_window(QMainWindow):

	def __init__(self):
		# Initialise the QMainWindow
		super().__init__()

		# Customise the QMainWindow
		self.initUI()
		self.settings = None

	def initUI(self):

		# Create the menubar and statusbar of the window
		menubar = self.menuBar()
		
		statusbar = self.statusBar()
		statusbar.showMessage('Ready')

		# Create the 'New Settings' Action
		newSettingsAct = QAction(QIcon('icons/newSettings.png'), '&New Settings', self)
		newSettingsAct.setShortcut('Ctrl+N')
		newSettingsAct.setStatusTip('Create New Settings')

		# Create the 'Import Settings' Action
		importSettingsAct = QAction(QIcon('icons/importSettings.png'), '&Import Settings', self)
		importSettingsAct.setShortcut('Ctrl+O')
		importSettingsAct.setStatusTip('Import Existing Settings')

		# Create the settings menu and add associated actions
		settingsMenu = menubar.addMenu('&Settings')
		settingsMenu.addAction(newSettingsAct)
		settingsMenu.addAction(importSettingsAct)

		# Create the settings toolbar and associated actions
		settingsToolbar = QToolBar(self)
		self.addToolBar(Qt.LeftToolBarArea, settingsToolbar)

		settingsToolbar.addAction(newSettingsAct)
		settingsToolbar.addAction(importSettingsAct)

		# Handle triggered 'NewSettings' and  'importSettings' actions
		newSettingsAct.triggered.connect(self.newSettingsTriggered)
		importSettingsAct.triggered.connect(self.importSettingsTriggered)

		# Set the attributes of the main window and display
		self.setGeometry(QDesktopWidget().availableGeometry())
		self.setWindowTitle('GARUDA - Sharp | Swift | Strong')
		# self.show()

		# Create and display contents of the main window
		main_widget = QWidget()
		self.setCentralWidget(main_widget)

		# create and display the 'GARUDA' logo
		garuda_footer_box = QHBoxLayout()

		garuda_logo_label = QLabel()
		garuda_logo_label.setPixmap(QPixmap('icons/garuda_small.png'))

		garuda_footer_box.addStretch()
		garuda_footer_box.addWidget(garuda_logo_label)

		
		# create and display widgets to read camera url
		self.camera_url_box = QHBoxLayout()

		camera_url_label = QLabel('Live Camera URL : ')
		self.camera_url_edit = QLineEdit()
		self.camera_capture_btn = QPushButton('Capture')

		self.camera_url_box.addWidget(camera_url_label)
		self.camera_url_box.addWidget(self.camera_url_edit)
		self.camera_url_box.addWidget(self.camera_capture_btn)


		# create and display widgets to display last seen component info
		last_comp_info_pane = QGroupBox('Last Component')

		last_comp_info_box = QVBoxLayout()

		self.last_comp_name_label  = QLabel('Component Name  :  {}'.format(None))
		self.last_comp_name_label.setStyleSheet('font-size: 12pt')
		self.last_comp_time_label  = QLabel('Timestamp             :  {}'.format(None))
		self.last_comp_time_label.setStyleSheet('font-size: 12pt')
		self.last_comp_match_label = QLabel('Match Percent        :  {}'.format(None))
		self.last_comp_match_label.setStyleSheet('font-size: 12pt')

		last_comp_info_box.addWidget(self.last_comp_name_label)
		last_comp_info_box.addWidget(self.last_comp_time_label)
		last_comp_info_box.addWidget(self.last_comp_match_label)

		last_comp_info_pane.setLayout(last_comp_info_box)

		# Create and display widgets to display live camera feed and last comp info
		self.camera_comp_info_box = QHBoxLayout()

		self.camera_feed_viewer = cameraFeedWidget()
		self.camera_comp_info_box.addStretch(1)
		self.camera_comp_info_box.addWidget(self.camera_feed_viewer)
		self.camera_comp_info_box.addStretch(3)
		self.camera_comp_info_box.addWidget(last_comp_info_pane)
		self.camera_comp_info_box.addStretch(1)

		# create and display main window layout
		self.main_box = QVBoxLayout()

		self.main_box.addLayout(garuda_footer_box)
		self.main_box.addStretch(1)
		

		main_widget.setLayout(self.main_box)

		# Handle 'capture' button pressed event
		self.camera_capture_btn.pressed.connect(self.startCapture)


	def newSettingsTriggered(self):
		
		setting_name, ok_pressed = QInputDialog.getText(self, 'New Settings Name', 'Enter a name for the <b>new setting</b>')
		
		if ok_pressed:
			
			if setting_name == '':
				QMessageBox.warning(self, 'Invalid Setting Name', '<b>Empty setting names are not allowed</b>. Please enter a setting name.')
				return

			if setting_name+".settings" in os.listdir('../.settings/'):
				QMessageBox.warning(self, 'Invalid Setting Name', 'The <b>setting name is already in use</b>. Please choose another setting name.')

			self.new_settings_wizard = fix_roi_window(setting_name)
			self.new_settings_wizard.show()


	def importSettingsTriggered(self):

		if os.listdir('../.settings/'):
			setting_name, button_pressed = QInputDialog.getItem(self, 'Import Settings', 'Choose setting to import', [setting_name[:-9] for setting_name in os.listdir('../.settings/') if setting_name.endswith('.settings')], 0, False)

			if button_pressed:
				
				setting_file = open('../.settings/'+setting_name+'.settings', 'rb')
				self.settings = pickle.load(setting_file)

				QMessageBox.information(self, 'Setting Imported', 'Setting <b>\'{}\'</b> was successfully imported.'.format(setting_name))

				self.main_box.addLayout(self.camera_url_box)
				self.main_box.addStretch(1)
				self.main_box.addLayout(self.camera_comp_info_box)
				self.main_box.addStretch(5)

		else:
			QMessageBox.warning(self, 'Empty Settings Set', '<b>No configured settings exist</b>. Please create a new setting and proceed.')


	def startCapture(self):

		camera_feed_url = self.camera_url_edit.text()

		if camera_feed_url.isdecimal():
			camera_feed_url = int(camera_feed_url)

		self.camera_feed_viewer.startVideoFeed(camera_feed_url, roi=self.settings['ROI'])
		self.camera_url_edit.setEnabled(False)
		self.camera_capture_btn.setEnabled(False)

		# Capture parts every 5s and identify the component
		self.capture_identify_timer = QTimer(self)
		self.capture_identify_timer.timeout.connect(self.identifyProduct)
		self.capture_identify_timer.start(5000)

	def identifyProduct(self):

		component_image = self.camera_feed_viewer.image_viewer.cv_image

		max_correlation = -1
		max_correlation_component = None

		for component_name in self.settings['Products']:
			correlation_value = correlation_coeff(gen_shape_descriptor(preprocess_image(component_image),10), self.settings['Products'][component_name])
			
			if correlation_value >= max_correlation:
				max_correlation = correlation_value
				max_correlation_component = component_name


		self.last_comp_name_label.setText("Component Name : "+max_correlation_component)
		self.last_comp_time_label.setText("Timestamp : "+QDateTime.currentDateTime().toString(Qt.ISODate))
		self.last_comp_match_label.setText("Match Percent : "+str(max_correlation))



	def closeEvent(self, event):

		# Stop the live camera feed
		self.camera_feed_viewer.stopVideoFeed()

# Test the home window
if __name__ == '__main__':

	# Create and display the application's home window
	application = QApplication(sys.argv)
	
	window = home_window()
	window.show()
	
	sys.exit(application.exec_())

