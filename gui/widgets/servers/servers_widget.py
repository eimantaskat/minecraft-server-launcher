from PyQt5.QtWidgets import (
	QHBoxLayout,
	QLabel,
	QVBoxLayout,
	QWidget,
	QTabWidget,
	QComboBox,
	QPushButton,
	QFormLayout,
	QSpinBox,
	QCheckBox,
	QLineEdit,
	QGroupBox,
	QScrollArea
)
from PyQt5.QtCore import Qt, QEventLoop

from gui import threads
from minecraft_server import VersionManager, exceptions
from gui.widgets.servers.servers_selection import ServerSelection
from gui.widgets.servers.server_settings_widget import ServerSettingsWidget
from gui.widgets.servers.server_properties_widget import ServerPropertiesWidget
from gui.widgets.combo_box import ComboBox
from minecraft_server.server import (
	Server,
	ServerSettings,
	server_properties,
	start_server,
	get_servers,
)
import os
import glob


class ServersWidget(QWidget):
	def __init__(self, parent):
		super().__init__()
		self.thread_handler = parent.thread_handler
		self.settings = parent.settings
		self.progress_bar = parent.progress_bar
		self.console_widget = parent.running_servers_widget.console_widget
		self.toolbar_widget = parent.toolbar_widget3
		self.versions_file = parent.settings.versions_file

		self.tabs = QTabWidget()
		self.tabs.addTab(self.start_servers_tab(), "Servers")
		self.tabs.addTab(self.create_new_server_tab(), "New server")

		self.servers_label = QLabel("Servers")

		self.layout = QVBoxLayout()
		self.layout.addWidget(self.servers_label)
		self.layout.addWidget(self.tabs)
		self.setLayout(self.layout)
		self.setContentsMargins(0, 0, 0, 0)


	def start_servers_tab(self):
		servers_tab = QWidget()
		servers_tab_layout = QVBoxLayout()
		servers_tab_layout.setAlignment(Qt.AlignTop)
		servers_tab.setLayout(servers_tab_layout)

		self.servers = get_servers(self.settings.data_location)
		self.servers_selection = ServerSelection(
			self.servers, self.thread_handler, start_server, self.console_widget, self.toolbar_widget)
		servers_tab_layout.addWidget(self.servers_selection)
		return servers_tab


	def create_new_server_tab(self):
		server_creation = QWidget()
		server_creation_layout = QVBoxLayout()
		server_creation.setLayout(server_creation_layout)

		versions = VersionManager.get_minecraft_versions(self.versions_file)

		self.header_layout = QHBoxLayout()

		self.version_select = ComboBox()
		self.version_select.addItems(versions)

		self.create_button = QPushButton("Create server")
		self.create_button.clicked.connect(self.create_server)

		self.settings_group = ServerSettingsWidget()

		self.config_group = ServerPropertiesWidget()

		self.name_lineedit = QLineEdit()
		self.name_lineedit.setText(f"Minecraft server")

		self.header_layout.addWidget(self.name_lineedit)
		self.header_layout.addWidget(self.version_select)

		server_creation_layout.addLayout(self.header_layout)
		server_creation_layout.addWidget(self.create_button)
		server_creation_layout.addWidget(self.settings_group)
		server_creation_layout.addWidget(self.config_group)

		servers_tab = QWidget()
		servers_tab_layout = QVBoxLayout()
		servers_tab_layout.setAlignment(Qt.AlignTop)
		servers_tab.setLayout(servers_tab_layout)
		servers_tab_layout.addWidget(server_creation)
		return servers_tab


	def refresh(self):
		self.servers = get_servers(self.settings.data_location)
		self.servers_selection.refresh(self.servers)
		print('refresh servers')


	def create_server(self):
		settings, properties = self.get_server_values()
		version = settings['version']

		server_data_path = os.path.join(
			self.settings.data_location, settings['name'])

		if os.path.exists(server_data_path):
			raise Exception("Server data path already exists")  # TODO

		os.makedirs(server_data_path)

		download_thread = threads.DownloadThread(version, server_data_path)
		download_thread.increment_progress_bar_value.connect(self.progress_bar.increment_value)
		download_thread.set_maximum_progress_bar_value.connect(self.progress_bar.set_maximum)
		download_thread.set_progress_bar_description.connect(self.progress_bar.set_description)
		download_thread.reset_progress_bar.connect(self.progress_bar.reset)
		download_thread.show_progress_bar.connect(self.progress_bar.show)

		loop = QEventLoop()
		download_thread.download_finished.connect(loop.quit)
		self.thread_handler.start_thread(download_thread)
		loop.exec_()

		self.progress_bar.start_loading()

		jar_pattern = '*.jar'
		jar_files = []
		jar_files = glob.glob(os.path.join(server_data_path, jar_pattern))

		# find jar file in server data path
		try:
			jar_path = jar_files[0]

			server_settings = ServerSettings(os.path.join(server_data_path, 'server.settings'), version)
			self.set_server_settings(server_settings, settings)
			server = Server(server_data_path, server_settings, jar_path)

			server_properties.create(server_data_path, properties)
			server.agree_to_eula()
		except IndexError:
			raise exceptions.JarNotFound("No jar file found in server data path")

		self.progress_bar.stop_loading()
		self.progress_bar.hide()

		self.refresh()


	def set_server_settings(self, server_settings: ServerSettings, settings: dict):
		for key, value in settings.items():
			setattr(server_settings, key, value)


	def get_server_values(self):
		# TODO: rewrite
		settings = {}

		settings['name'] = self.name_lineedit.text()
		settings['version'] = self.version_select.currentText()

		settings_widgets = self.settings_group.settings_widgets
		settings_keys = settings_widgets.keys()
		for key in settings_keys:
			widget = settings_widgets[key]
			if isinstance(widget, QSpinBox):
				settings[key] = widget.value()
			elif isinstance(widget, QCheckBox):
				settings[key] = widget.isChecked()
			elif isinstance(widget, QLineEdit):
				settings[key] = widget.text()

		properties = {}

		properties_widgets = self.config_group.properties_widgets
		properties_keys = properties_widgets.keys()
		for key in properties_keys:
			widget = properties_widgets[key]
			if isinstance(widget, QSpinBox):
				properties[key] = widget.value()
			elif isinstance(widget, QCheckBox):
				properties[key] = widget.isChecked()
			elif isinstance(widget, QLineEdit):
				properties[key] = widget.text()
			elif isinstance(widget, QComboBox):
				properties[key] = widget.currentText()

		properties = server_properties.stringify(properties)
		return settings, properties
