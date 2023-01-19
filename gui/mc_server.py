from PyQt5.QtWidgets import QMainWindow, QAction, QStackedWidget, QLabel, QVBoxLayout, QWidget, QToolBar, QComboBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from .widgets import ToolbarItem, SettingsWidget
from . import threads
from minecraft_server import Settings, get_servers, version


class MinecraftServerLauncher(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the ThreadHandler
        self.thread_handler = threads.ThreadHandler()
        self.settings = Settings()
        self.settings.load_settings()

        # servers = get_servers(self.settings.data_location)

        # for server in servers:
        #     self.thread_handler.add_thread(threads.ServerThread, server)

        # Set window properties
        self.setWindowTitle("Minecraft Server Launcher")
        self.setGeometry(100, 100, 800, 600)

        # Create and configure toolbar
        self.create_toolbar()

        # Create stacked widget and add content
        self.create_stacked_widget()

        self.stack.setCurrentIndex(1)

    def create_toolbar(self):
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setOrientation(Qt.Vertical)
        self.toolbar.setIconSize(QSize(40, 40))
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        # Create icons for toolbar
        icon1 = QIcon("assets/icon1.png")
        icon2 = QIcon("assets/icon2.png")
        icon3 = QIcon("assets/icon3.png")

        # Create actions for toolbar
        self.action1 = QAction(icon1, "Settings", self)
        self.action2 = QAction(icon2, "Servers", self)
        self.action3 = QAction(icon3, "Running servers", self)

        toolbar_widget1 = ToolbarItem(self.action1, icon1, "Settings")
        toolbar_widget2 = ToolbarItem(self.action2, icon2, "Servers", True)
        toolbar_widget3 = ToolbarItem(self.action3, icon3, "Running servers")

        # Add actions to toolbar
        self.toolbar.addWidget(toolbar_widget1)
        self.toolbar.addWidget(toolbar_widget2)
        self.toolbar.addWidget(toolbar_widget3)

    def create_stacked_widget(self):
        self.stack = QStackedWidget(self)

        # Create widgets for stack
        widget1 = QWidget()
        layout1 = QVBoxLayout(widget1)
        settings_widget = SettingsWidget(self.settings)
        layout1.addWidget(settings_widget)
        
        widget2 = QWidget()
        layout2 = QVBoxLayout(widget2)
        servers_widget = ServersWidget(self.settings, self.thread_handler)
        layout2.addWidget(servers_widget)

        widget3 = QWidget()
        layout3 = QVBoxLayout(widget3)
        layout3.addWidget(QLabel("Content for option 3"))

        # Add widgets to stack
        self.stack.addWidget(widget1)
        self.stack.addWidget(widget2)
        self.stack.addWidget(widget3)

        # Set stack as central widget
        self.setCentralWidget(self.stack)

        # Connect actions to stacked widget
        self.action1.triggered.connect(lambda: self.stack.setCurrentIndex(0))
        self.action2.triggered.connect(lambda: self.stack.setCurrentIndex(1))
        self.action3.triggered.connect(lambda: self.stack.setCurrentIndex(2))

    def _download_handler(self):
        jar_version = self.jar_version_combo.currentText()
        download_location = self.download_location_edit.text()
        self.thread_handler.add_thread(
            threads.DownloadThread, jar_version, download_location)


    def closeEvent(self, event):
        # Stop download thread
        self.thread_handler.stop_threads_by_class(threads.DownloadThread)
        # Stop server threads
        server_threads = self.thread_handler.get_threads_by_class(threads.ServerThread)
        for server_thread in server_threads:
            server_thread.stop()
            
        # Wait for the rest to finish
        self.thread_handler.wait_for_all_threads()


from PyQt5.QtWidgets import QTabWidget, QHBoxLayout, QGridLayout
# from PyQt5.QtGui import
# from PyQt5.QtCore import

class ServersWidget(QWidget):
    def __init__(self, settings: Settings, thread_handler: threads.ThreadHandler):
        super().__init__()
        self.thread_handler = thread_handler
        self.settings = settings

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_servers_tab(), "Servers")
        self.tabs.addTab(self.create_new_server_tab(), "New server")

        self.servers_label = QLabel("Servers")
        self.servers_label.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.servers_label)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.setContentsMargins(0, 0, 0, 0)

    def create_servers_tab(self):
        servers_selection = QWidget()
        servers_selection_layout = QGridLayout()
        servers_selection.setLayout(servers_selection_layout)

        servers = get_servers(self.settings.data_location)
        servers = [f"{server.server_version_name}: {server.name}" for server in servers]

        self.server_select = QComboBox()
        self.server_select.addItems(servers)

        self.start_button = QPushButton("Start Server")
        self.start_button.clicked.connect(self.start_server)

        servers_selection_layout.addWidget(self.server_select, 0, 0)
        servers_selection_layout.addWidget(self.start_button, 0, 1)

        servers_tab = QWidget()
        servers_tab_layout = QVBoxLayout()
        servers_tab.setLayout(servers_tab_layout)
        servers_tab_layout.addWidget(servers_selection)
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
        servers_tab.setLayout(servers_tab_layout)
        servers_tab_layout.addWidget(server_creation)
        return servers_tab


    def create_server(self):
        selected_version = self.version_select.currentText()
        print(f"called create with version {selected_version}")

    def start_server(self):
        running_servers = self.thread_handler.get_threads_by_class(threads.ServerThread)
        if running_servers:
            return print("Server is already running!") # TODO

        selected_index = self.server_select.currentIndex()
        servers = get_servers(self.settings.data_location)
        selected_server = servers[selected_index]
        self.thread_handler.add_thread(threads.ServerThread, selected_server)