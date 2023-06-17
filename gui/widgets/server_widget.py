from PyQt5.QtWidgets import (QAction, QFileDialog, QHBoxLayout, QLabel, QMenu,
							 QPushButton, QSizePolicy, QVBoxLayout, QWidget)
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QFont


class ServerWidget(QWidget):
	def __init__(self, server_info):
		super().__init__()
		self.server_info = server_info

		layout = QHBoxLayout(self)

		# Title Layout
		title_layout = QVBoxLayout()

		name_font = QFont()
		name_font.setBold(True)

		# Server Name Label
		name_label = QLabel(server_info.name)
		name_label.setFont(name_font)
		title_layout.addWidget(name_label)

		# Server Version Label
		version_label = QLabel(f"Version: {server_info.server_version_name}")
		title_layout.addWidget(version_label)

		layout.addLayout(title_layout)

		# Start Button
		start_button = QPushButton("Start")
		start_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		start_button.clicked.connect(self.start_server)
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

	def start_server(self):
		# Implement server start logic here
		pass

	def open_folder(self):
		path = self.server_info.path
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
		# Implement edit server logic here
		pass

	def duplicate_server(self):
		# Implement duplicate server logic here
		pass

	def delete_server(self):
		# Implement delete server logic here
		pass
