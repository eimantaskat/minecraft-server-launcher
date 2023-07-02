import json
import os
import shutil

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QAction, QFileDialog, QHBoxLayout, QLabel, QMenu,
                             QPushButton, QSizePolicy, QVBoxLayout, QWidget)

from gui.widgets.full_window_widget import FullWindowWidget
from gui.widgets.servers.server_properties_widget import ServerPropertiesWidget
from gui.widgets.servers.server_settings_widget import ServerSettingsWidget
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
		edit_server_widget = self.create_edit_server_widget()
		self.new_server_widget = FullWindowWidget(self, widget=edit_server_widget)
		self.new_server_widget.show()

	def duplicate_server(self):
		# Create a new folder path for the duplicated server
		duplicated_server_path = self.server.path + " copy"
		copy_number = 1

		while os.path.exists(duplicated_server_path):
			# Append copy number to the folder name
			duplicated_server_path = self.server.path + f" copy ({copy_number})"
			copy_number += 1

		try:
			# Duplicate the server folder
			shutil.copytree(self.server.path, duplicated_server_path)

			# Update the name in server.settings file
			settings_file_path = os.path.join(duplicated_server_path, "server.settings")
			with open(settings_file_path, 'r') as settings_file:
				settings = json.load(settings_file)
			
			settings["name"] = f"{self.server.name} copy"
			
			with open(settings_file_path, 'w') as settings_file:
				json.dump(settings, settings_file, indent=4)

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

	def create_edit_server_widget(self):
		server_creation = QWidget()
		server_creation_layout = QVBoxLayout()
		server_creation.setLayout(server_creation_layout)

		self.header_layout = QHBoxLayout()

		self.save_button = QPushButton("Save")
		self.save_button.clicked.connect(self.save_server)

		self.settings_group = ServerSettingsWidget(self, self.server.path)

		self.properties_group = ServerPropertiesWidget(self, self.server.path)

		server_creation_layout.addLayout(self.header_layout)
		server_creation_layout.addWidget(self.settings_group)
		server_creation_layout.addWidget(self.properties_group)
		server_creation_layout.addWidget(self.save_button)

		servers_widget = QWidget()
		servers_widget_layout = QVBoxLayout()
		servers_widget_layout.setAlignment(Qt.AlignTop)
		servers_widget.setLayout(servers_widget_layout)
		servers_widget_layout.addWidget(server_creation)
		return servers_widget
	
	def save_server(self):
		self.settings_group.save_settings()
		self.properties_group.save_properties(new_path=self.settings_group.server_path)
		self.new_server_widget.destroy()
		self.parent.refresh()