from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QTabWidget, QVBoxLayout, QWidget

from gui.widgets import ConsoleWidget


class RunningServersWidget(QWidget):
	def __init__(self):
		super().__init__()

		self.tabs = QTabWidget()
		self.tabs.addTab(self.create_console_tab(), "Console")
		self.tabs.addTab(self.create_settings_tab(), "Settings")

		self.servers_label = QLabel("Running servers")

		self.layout = QVBoxLayout()
		self.layout.addWidget(self.servers_label)
		self.layout.addWidget(self.tabs)
		self.setLayout(self.layout)
		self.setContentsMargins(0, 0, 0, 0)

	def create_console_tab(self):
		self.console_widget = ConsoleWidget()

		console_tab = QWidget()
		console_tab_layout = QVBoxLayout()
		console_tab_layout.setAlignment(Qt.AlignTop)
		console_tab_layout.addWidget(self.console_widget)
		console_tab.setLayout(console_tab_layout)
		
		return console_tab

	def create_settings_tab(self):
		settings_tab = QWidget()
		settings_tab_layout = QVBoxLayout()
		settings_tab_layout.setAlignment(Qt.AlignTop)
		# settings_tab_layout.addWidget()
		settings_tab.setLayout(settings_tab_layout)
		
		return settings_tab
