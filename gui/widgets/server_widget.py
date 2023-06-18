import shutil

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QAction, QFileDialog, QHBoxLayout, QLabel, QMenu,
                             QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from minecraft_server.server import start_server


class ServerWidget(QWidget):
	def __init__(self, parent, server):
		super().__init__()
		self.parent = parent
		self.main_window = parent.main_window
		self.thread_handler = parent.thread_handler
		self.console_widget = parent.console_widget
		self.toolbar_widget = parent.toolbar_widget

		self.server = server

		layout = QHBoxLayout(self)

		# Title Layout
		title_layout = QVBoxLayout()

		name_font = QFont()
		name_font.setBold(True)

		# Server Name Label
		name_label = QLabel(server.name)
		name_label.setFont(name_font)
		title_layout.addWidget(name_label)

		# Server Version Label
		version_label = QLabel(f"Version: {server.server_version_name}")
		title_layout.addWidget(version_label)

		layout.addLayout(title_layout)

		# Start Button
		start_button = QPushButton("Start")
		start_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		start_button.clicked.connect(self.button_start_server)
		layout.addWidget(start_button)

		# Folder Button
		folder_button = QPushButton("Folder")
		folder_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		folder_button.clicked.connect(self.open_folder)
		layout.addWidget(folder_button)

		# More Options Button
		more_button = QPushButton("...")
		more_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		more_button.clicked.connect(self.show_options)
		layout.addWidget(more_button)

	def button_start_server(self):
		start_server(self.thread_handler, self.server,
		             self.console_widget, self.toolbar_widget)

	def open_folder(self):
		path = self.server.path
		QFileDialog.getOpenFileUrl(self, 'Open Folder', QUrl.fromLocalFile(path))

	def show_options(self):
		menu = QMenu(self)

		# Edit Action
		edit_action = QAction("Edit", self)
		edit_action.triggered.connect(self.edit_server)
		menu.addAction(edit_action)

		# Duplicate Action
		duplicate_action = QAction("Duplicate", self)
		duplicate_action.triggered.connect(self.duplicate_server)
		menu.addAction(duplicate_action)

		# Delete Action
		delete_action = QAction("Delete", self)
		delete_action.triggered.connect(self.delete_server)
		menu.addAction(delete_action)

		menu.exec_(self.mapToGlobal(self.sender().pos()))

	def edit_server(self):
		# TODO: Implement edit server logic here
		pass

	def duplicate_server(self):
		# Create a new folder path for the duplicated server
		duplicated_server_path = self.server.path + " copy"

		try:
			# Duplicate the server folder
			shutil.copytree(self.server.path, duplicated_server_path)
			
			# Refresh the parent widget
			self.parent.refresh()
			
		except Exception as e:
			# Handle any errors that may occur during the duplication process
			print("Error duplicating server:", str(e))

	def delete_server(self):
		# TODO: Add a confirmation dialog before deleting the server
		try:
			# Delete the server folder
			shutil.rmtree(self.server.path)
			
			# Refresh the parent widget
			self.parent.refresh()
			
		except Exception as e:
			# Handle any errors that may occur during the deletion process
			print("Error deleting server:", str(e))
