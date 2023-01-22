from PyQt5.QtWidgets import QMainWindow, QAction, QStackedWidget, QLabel, QVBoxLayout, QWidget, QToolBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from .widgets import ToolbarItem, SettingsWidget, ServersWidget
from . import threads
from minecraft_server import Settings


class MinecraftServerLauncher(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the ThreadHandler
        self.thread_handler = threads.ThreadHandler()
        self.settings = Settings()
        self.settings.settings_changed.connect(self.refresh_widgets)
        self.settings.load_settings()

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
        self.settings_widget = SettingsWidget(self.settings)
        layout1.addWidget(self.settings_widget)
        
        widget2 = QWidget()
        layout2 = QVBoxLayout(widget2)
        self.servers_widget = ServersWidget(self.settings, self.thread_handler)
        layout2.addWidget(self.servers_widget)

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

    def refresh_widgets(self):
        # update servers widget
        try:
            self.servers_widget.refresh()
        except AttributeError:
            pass
