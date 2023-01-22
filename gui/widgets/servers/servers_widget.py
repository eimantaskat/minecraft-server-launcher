from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget, QTabWidget, QComboBox, QPushButton, QFormLayout, QSpinBox, QCheckBox, QLineEdit, QGroupBox
from PyQt5.QtCore import Qt
from ... import threads
from minecraft_server import Settings, version
from .servers_selection import ServerSelection
from minecraft_server.server import start_server, get_servers, get_default_settings

class ServersWidget(QWidget):
    def __init__(self, settings: Settings, thread_handler: threads.ThreadHandler):
        super().__init__()
        self.thread_handler = thread_handler
        self.settings = settings

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_servers_tab(), "Servers")
        self.tabs.addTab(self.create_new_server_tab(), "New server")

        self.servers_label = QLabel("Servers")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.servers_label)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)

    def create_servers_tab(self):
        servers_tab = QWidget()
        servers_tab_layout = QVBoxLayout()
        servers_tab_layout.setAlignment(Qt.AlignTop)
        servers_tab.setLayout(servers_tab_layout)

        self.servers = get_servers(self.settings.data_location)
        self.servers_selection = ServerSelection(self.servers, self.thread_handler, start_server)
        servers_tab_layout.addWidget(self.servers_selection)
        return servers_tab


    def create_new_server_tab(self):
        server_creation = QWidget()
        server_creation_layout = QVBoxLayout()
        server_creation.setLayout(server_creation_layout)

        versions = version.get_minecraft_versions()

        self.header_layout = QHBoxLayout()

        self.version_select = QComboBox()
        self.version_select.addItems(versions)

        self.start_button = QPushButton("Create server")
        self.start_button.clicked.connect(self.create_server)

        self.settings_group = QGroupBox("Server Settings")
        self.settings_layout = self.create_settings_layout()
        self.settings_group.setLayout(self.settings_layout)

        self.name_lineedit = QLineEdit()
        self.name_lineedit.setText(f"Minecraft server")

        
        self.header_layout.addWidget(self.name_lineedit)
        self.header_layout.addWidget(self.version_select)

        server_creation_layout.addLayout(self.header_layout)
        server_creation_layout.addWidget(self.start_button)
        server_creation_layout.addWidget(self.settings_group)

        servers_tab = QWidget()
        servers_tab_layout = QVBoxLayout()
        servers_tab_layout.setAlignment(Qt.AlignTop)
        servers_tab.setLayout(servers_tab_layout)
        servers_tab_layout.addWidget(server_creation)
        return servers_tab

    def create_settings_layout(self):
        form_layout = QFormLayout()
        server_settings = get_default_settings()

        # version = self.version_select.currentText()

        # create widgets for each setting
        self.Xmx_spinbox = QSpinBox()
        self.Xmx_spinbox.setRange(0, 2147483647)
        self.Xmx_spinbox.setValue(server_settings['_Xmx'])
        self.Xms_spinbox = QSpinBox()
        self.Xms_spinbox.setRange(0, 2147483647)
        self.Xms_spinbox.setValue(server_settings['_Xms'])
        self.bonusChest_checkbox = QCheckBox()
        self.bonusChest_checkbox.setChecked(server_settings['_bonusChest'])
        self.eraseCache_checkbox = QCheckBox()
        self.eraseCache_checkbox.setChecked(server_settings['_eraseCache'])
        self.forceUpgrade_checkbox = QCheckBox()
        self.forceUpgrade_checkbox.setChecked(server_settings['_forceUpgrade'])
        # self.initSettings_checkbox = QCheckBox()
        # self.initSettings_checkbox.setChecked(server_settings['_initSettings'])
        # self.port_spinbox = QSpinBox()
        # self.port_spinbox.setRange(0, 65536)
        # self.port_spinbox.setValue(server_settings['_port'])
        self.safeMode_checkbox = QCheckBox()
        self.safeMode_checkbox.setChecked(server_settings['_safeMode'])
        self.universe_lineedit = QLineEdit()
        self.universe_lineedit.setText(server_settings['_universe'])
        self.world_lineedit = QLineEdit()
        self.world_lineedit.setText(server_settings['_world'])

        # add widgets to form layout
        form_layout.addRow("Xmx (MB)", self.Xmx_spinbox)
        form_layout.addRow("Xms (MB)", self.Xms_spinbox)
        form_layout.addRow("Generate bonus chest", self.bonusChest_checkbox)
        form_layout.addRow("Erase cache", self.eraseCache_checkbox)
        form_layout.addRow("Force upgrade", self.forceUpgrade_checkbox)
        # form_layout.addRow("Load settings from file", self.initSettings_checkbox)
        # form_layout.addRow("Port", self.port_spinbox)
        form_layout.addRow("Load level with vanilla datapack only", self.safeMode_checkbox)
        form_layout.addRow("Universe folder", self.universe_lineedit)
        form_layout.addRow("World folder", self.world_lineedit)

        return form_layout

    def refresh(self):
        self.servers = get_servers(self.settings.data_location)
        self.servers_selection.refresh(self.servers)
        print('refresh servers')

    def create_server(self):
        selected_version = self.version_select.currentText()
        print(f"called create with version {selected_version}")