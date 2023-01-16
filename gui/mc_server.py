from PyQt5.QtWidgets import QMainWindow, QAction, QStackedWidget, QLabel, QVBoxLayout, QWidget, QToolBar, QPushButton, QFileDialog, QHBoxLayout, QTabWidget, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from .widgets import ToolbarItem
from . import threads
import os


class MinecraftServerLauncher(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the ThreadHandler
        self.thread_handler = threads.ThreadHandler()

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
        settings_widget = SettingsWidget()
        layout1.addWidget(settings_widget)
        widget2 = QWidget()
        layout2 = QVBoxLayout(widget2)
        layout2.addWidget(QLabel("Content for option 2"))
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
        # Wait for the rest to finish
        self.thread_handler.wait_for_all_threads()

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
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
        # Create widgets for general tab
        general_tab = QWidget()

        # Set layout for general tab
        general_tab_layout = QVBoxLayout()
        general_tab.setLayout(general_tab_layout)
        return general_tab

    def create_server_tab(self):
        # Create widgets for server tab
        server_tab = QWidget()
        # Set layout for server tab
        server_tab_layout = QVBoxLayout()
        server_tab.setLayout(server_tab_layout)
        
        self.set_data_location_label = QLabel("Data Location:")
        self.set_data_location_button = QPushButton("Select Folder")
        self.reset_data_location_button = QPushButton("Set to default")
        self.set_data_location_button.clicked.connect(self.set_data_location)
        self.reset_data_location_button.clicked.connect(self.reset_data_location)
        self.data_location_layout = QHBoxLayout()
        self.data_location_layout.addWidget(self.set_data_location_label)
        self.data_location_layout.addWidget(self.set_data_location_button)
        self.data_location_layout.addWidget(self.reset_data_location_button)
        server_tab_layout.addLayout(self.data_location_layout)
        self.data_location = f"{os.getenv('APPDATA')}/.minecraft-server"
        self.set_data_location_label.setText(f"Data Location: {self.data_location}")

        return server_tab

    def create_about_tab(self):
        # Create widgets for about tab
        about_tab = QWidget()
        # Set layout for about tab
        about_tab_layout = QVBoxLayout()
        about_tab.setLayout(about_tab_layout)
        return about_tab

    def set_data_location(self):
        self.data_location = QFileDialog.getExistingDirectory()
        if not self.data_location:
            self.data_location = f"{os.getenv('APPDATA')}/.minecraft-server"
        self.set_data_location_label.setText("Data Location: " + self.data_location)

    def reset_data_location(self):
        self.data_location = f"{os.getenv('APPDATA')}/.minecraft-server"
        self.set_data_location_label.setText("Data Location: " + self.data_location)
