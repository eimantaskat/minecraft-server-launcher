import json
import os

from PyQt5.QtWidgets import (QCheckBox, QFormLayout, QGroupBox, QLineEdit,
                             QSpinBox, QVBoxLayout, QWidget)


class ServerSettingsWidget(QWidget):
	def __init__(self, parent, server_path=None):
		super().__init__()
		self.parent = parent
		self.main_window = parent.main_window

		self.__config_file = 'default_server_config.json'

		self.server_path = server_path
		self._get_server_settings()
		self.create_settings_layout()

		self.settings_group = QGroupBox('Server Settings')
		self.settings_group.setLayout(self.settings_layout)

		layout = QVBoxLayout()
		layout.addWidget(self.settings_group)
		self.setLayout(layout)

	def _read_server_settings(self):
		with open(self.server_path + '/server.settings', 'r') as file:
			self.server_settings = json.load(file)

	def _get_server_settings(self):
		if self.server_path:
			self._read_server_settings()

	def save(self):
		# Update the name in server_settings if necessary
		folder_name = os.path.basename(self.server_path)
		if folder_name != self.server_settings['name']:
			new_folder_path = os.path.join(os.path.dirname(self.server_path), self.server_settings['name'])
			
			try:
				# Rename the folder
				os.rename(self.server_path, new_folder_path)
				self.server_path = new_folder_path
			except OSError as e:
				print(f"Error renaming folder: {str(e)}")
				return

		with open(self.server_path + '/server.settings', 'w') as file:
			json.dump(self.server_settings, file)

	@staticmethod
	def update_setting_values(dict_list, default_values):
		# TODO: Remove duplicate code
		for item in dict_list:
			key = item['key']
			if key in default_values:
				item['value'] = default_values[key]
		return dict_list

	def create_settings_layout(self):
		self.settings_layout = QFormLayout()

		self.settings_widgets = {}


		with open(self.__config_file, 'r') as file:
			config = json.load(file)
			settings_config = config['settings']

		if self.server_path:
			self.update_setting_values(settings_config, self.server_settings)

		for setting in settings_config:
			setting_key = setting['key']
			setting_name = setting['name']
			setting_type = setting['type']
			setting_value = setting['value']

			if setting_type == 'spinbox':
				self.settings_widgets[setting_key] = QSpinBox()
				min_value = setting['min_value']
				max_value = setting['max_value']
				self.settings_widgets[setting_key].setRange(min_value, max_value)
				self.settings_widgets[setting_key].setValue(setting_value)
			elif setting_type == 'checkbox':
				self.settings_widgets[setting_key] = QCheckBox()
				self.settings_widgets[setting_key].setChecked(setting_value)
			elif setting_type == 'lineedit':
				self.settings_widgets[setting_key] = QLineEdit()
				self.settings_widgets[setting_key].setText(setting_value)

			self.settings_layout.addRow(setting_name,
										self.settings_widgets[setting_key])
	
	def get_settings(self):
		settings = {}

		settings_widgets = self.settings_widgets
		settings_keys = settings_widgets.keys()
		for key in settings_keys:
			widget = settings_widgets[key]
			if isinstance(widget, QSpinBox):
				settings[key] = widget.value()
			elif isinstance(widget, QCheckBox):
				settings[key] = widget.isChecked()
			elif isinstance(widget, QLineEdit):
				settings[key] = widget.text()
		return settings
	
	def save_settings(self):
		settings = self.get_settings()
		self.server_settings = settings
		self.save()