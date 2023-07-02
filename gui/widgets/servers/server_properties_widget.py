import json

from PyQt5.QtWidgets import (QCheckBox, QComboBox, QFormLayout, QGroupBox,
                             QLineEdit, QScrollArea, QSpinBox, QVBoxLayout,
                             QWidget)

from gui.widgets.combo_box import ComboBox
from gui.widgets.spin_box import SpinBox
from minecraft_server.server import ServerProperties


class ServerPropertiesWidget(QWidget):
	def __init__(self, parent, server_path=None):
		super().__init__()
		self.parent = parent
		self.main_window = parent.main_window

		self.__config_file = 'default_server_config.json'

		self.server_path = server_path
		self.server_properties = ServerProperties(self.server_path)
		self.create_properties_layout()

		self.config_group = QGroupBox("Server configuration")
		self.config_group.setLayout(QVBoxLayout())
		self.config_group.layout().addWidget(self.config_scroll_area)

		layout = QVBoxLayout()
		layout.addWidget(self.config_group)
		self.setLayout(layout)

	@staticmethod
	def update_setting_values(dict_list, default_values):
		# TODO: Remove duplicate code
		for item in dict_list:
			key = item['key']
			if key in default_values:
				item['value'] = default_values[key]
		return dict_list

	def create_properties_layout(self):
		properties_layout = QFormLayout()
		
		self.properties_widgets = {}

		with open(self.__config_file, 'r') as file:
			config = json.load(file)
			properties_config = config['properties']

		if self.server_path:
			self.update_setting_values(properties_config, self.server_properties.properties)

		for property in properties_config:
			property_key = property['key']
			property_name = property['name']
			property_type = property['type']
			property_value = property['value']

			if property_type == 'spinbox':
				self.properties_widgets[property_key] = SpinBox()
				min_value = property['min_value']
				max_value = property['max_value']
				self.properties_widgets[property_key].setRange(min_value, max_value)
				self.properties_widgets[property_key].setValue(property_value)
			elif property_type == 'checkbox':
				self.properties_widgets[property_key] = QCheckBox()
				self.properties_widgets[property_key].setChecked(property_value)
			elif property_type == 'combobox':
				self.properties_widgets[property_key] = ComboBox()
				self.properties_widgets[property_key].addItems(property['values'])
				self.properties_widgets[property_key].setCurrentText(property_value)
			elif property_type == 'lineedit':
				self.properties_widgets[property_key] = QLineEdit()
				self.properties_widgets[property_key].setText(property_value)

			properties_layout.addRow(property_name, self.properties_widgets[property_key])

		container_widget = QWidget()
		container_widget.setLayout(properties_layout)

		self.config_scroll_area = QScrollArea()
		self.config_scroll_area.setWidget(container_widget)
		self.config_scroll_area.setWidgetResizable(True)

		return self.config_scroll_area

	def save_properties(self):
		properties = {}

		properties_widgets = self.properties_widgets
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

		self.server_properties.properties = properties
		self.server_properties.write()
