from PyQt5.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget, QTabWidget, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from ... import threads
from minecraft_server import Settings, version
from .servers_selection import ServerSelection
from minecraft_server.server import start_server, get_servers

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
        server_creation_layout = QGridLayout()
        server_creation.setLayout(server_creation_layout)

        versions = version.get_minecraft_versions()

        self.version_select = QComboBox()
        self.version_select.addItems(versions)

        self.start_button = QPushButton("Create server")
        self.start_button.clicked.connect(self.create_server)

        server_creation_layout.addWidget(self.version_select, 0, 0)
        server_creation_layout.addWidget(self.start_button, 0, 1)

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
        selected_version = self.version_select.currentText()
        print(f"called create with version {selected_version}")