from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTabWidget, QCheckBox, QGridLayout
from PyQt5.QtCore import Qt
from minecraft_server import Settings
import os


class SettingsWidget(QWidget):
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_general_tab(), "General")
        self.tabs.addTab(self.create_server_tab(), "Server")
        self.tabs.addTab(self.create_about_tab(), "About")

        self.settings_label = QLabel("Settings")
        self.settings_label.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.settings_label)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)


    def create_general_tab(self):
        general_tab = QWidget()
        general_tab_layout = QVBoxLayout()
        general_tab_layout.setAlignment(Qt.AlignTop)
        general_tab.setLayout(general_tab_layout)
        return general_tab


    def create_server_tab(self):
        server_tab = QWidget()
        server_tab_layout = QGridLayout()
        server_tab_layout.setAlignment(Qt.AlignTop)
        server_tab.setLayout(server_tab_layout)

        # data location settings
        self.data_location_label = QLabel("Servers Data Location:")
        self.data_location_value = QLabel(
            os.path.expandvars(self.settings.data_location))
        self.set_data_location_button = QPushButton("Select Folder")
        self.reset_data_location_button = QPushButton("Set to default")
        self.set_data_location_button.clicked.connect(self.set_data_location)
        self.reset_data_location_button.clicked.connect(
            self.reset_data_location)

        # auto-start option
        self.auto_start_label = QLabel("Auto-start server:")
        self.auto_start_checkbox = QCheckBox()
        self.auto_start_checkbox.setChecked(self.settings.auto_start)
        self.auto_start_checkbox.stateChanged.connect(
            self.handle_auto_start_change)

        # add the widgets to the grid layout
        server_tab_layout.addWidget(self.data_location_label, 0, 0)
        server_tab_layout.addWidget(self.data_location_value, 1, 0)
        server_tab_layout.addWidget(self.set_data_location_button, 1, 1)
        server_tab_layout.addWidget(self.reset_data_location_button, 1, 2)
        server_tab_layout.addWidget(self.auto_start_label, 2, 0)
        server_tab_layout.addWidget(self.auto_start_checkbox, 2, 1)

        return server_tab


    def create_about_tab(self):
        about_tab = QWidget()
        about_tab_layout = QVBoxLayout()
        about_tab_layout.setAlignment(Qt.AlignTop)
        about_tab.setLayout(about_tab_layout)
        return about_tab


    def set_data_location(self):
        self.data_location = QFileDialog.getExistingDirectory()
        if not self.data_location:
            default_settings = self.settings.get_default_settings()
            self.data_location = default_settings['_data_location']
        self.settings.data_location = self.data_location
        self.data_location_value.setText(self.data_location)


    def reset_data_location(self):
        default_settings = self.settings.get_default_settings()
        self.data_location = default_settings['_data_location']
        self.settings.data_location = self.data_location
        self.data_location_value.setText(self.data_location)


    def handle_auto_start_change(self, state):
        if state == Qt.Checked:
            self.settings.auto_start = True
        else:
            self.settings.auto_start = False
