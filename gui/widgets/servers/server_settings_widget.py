from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QFormLayout,
    QSpinBox,
    QCheckBox,
    QLineEdit,
    QGroupBox,
)
from minecraft_server.server import get_default_settings
import json


class ServerSettingsWidget(QWidget):
    def __init__(self, server_path=None, parent=None):
        super().__init__()

        self.server_path = server_path
        self._get_server_settings()
        self.create_settings_layout()

        self.settings_group = QGroupBox("Server Settings")
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
        else:
            self.server_settings = get_default_settings()


    def create_settings_layout(self):
        self.settings_layout = QFormLayout()

        # create widgets for each setting
        self.Xmx_spinbox = QSpinBox()
        self.Xmx_spinbox.setRange(0, 2147483647)
        self.Xmx_spinbox.setValue(self.server_settings['_Xmx'])
        self.Xms_spinbox = QSpinBox()
        self.Xms_spinbox.setRange(0, 2147483647)
        self.Xms_spinbox.setValue(self.server_settings['_Xms'])
        self.bonus_chest_checkbox = QCheckBox()
        self.bonus_chest_checkbox.setChecked(self.server_settings['_bonusChest'])
        self.erase_cache_checkbox = QCheckBox()
        self.erase_cache_checkbox.setChecked(self.server_settings['_eraseCache'])
        self.force_upgrade_checkbox = QCheckBox()
        self.force_upgrade_checkbox.setChecked(self.server_settings['_forceUpgrade'])
        self.safe_mode_checkbox = QCheckBox()
        self.safe_mode_checkbox.setChecked(self.server_settings['_safeMode'])
        self.universe_lineedit = QLineEdit()
        self.universe_lineedit.setText(self.server_settings['_universe'])

        # add widgets to form layout
        self.settings_layout.addRow("Xmx (MB)", self.Xmx_spinbox)
        self.settings_layout.addRow("Xms (MB)", self.Xms_spinbox)
        self.settings_layout.addRow("Generate bonus chest", self.bonus_chest_checkbox)
        self.settings_layout.addRow("Erase cache", self.erase_cache_checkbox)
        self.settings_layout.addRow("Force upgrade", self.force_upgrade_checkbox)
        self.settings_layout.addRow("Load level with vanilla datapack only",
                        self.safe_mode_checkbox)
        self.settings_layout.addRow("Universe folder", self.universe_lineedit)
