from PyQt5.QtWidgets import QMainWindow, QAction, QStackedWidget, QVBoxLayout, QWidget, QToolBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QEventLoop, QTimer
from gui.widgets import ToolbarItem, SettingsWidget, ServersWidget, ProgressBar, RunningServersWidget
from gui import threads
from minecraft_server import Settings, VersionManager


class MinecraftServerLauncher(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the ThreadHandler
        self.thread_handler = threads.ThreadHandler()
        self.settings = Settings()
        self.settings.settings_changed.connect(self.refresh_widgets)
        self.settings.load_settings()

        # Update cached versions
        VersionManager.update_cached_versions(self.settings.versions_file)

        # Set window properties
        self.setWindowTitle("Minecraft Server Launcher")
        self.setGeometry(100, 100, 800, 600)

        # Create progress bar
        self.progress_bar = ProgressBar()
        self.progress_bar.hide()

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

        self.toolbar_widget1 = ToolbarItem(self.action1, icon1, "Settings")
        self.toolbar_widget2 = ToolbarItem(self.action2, icon2, "Servers", True)
        self.toolbar_widget3 = ToolbarItem(self.action3, icon3, "Running servers")

        # Add actions to toolbar
        self.toolbar.addWidget(self.toolbar_widget1)
        self.toolbar.addWidget(self.toolbar_widget2)
        self.toolbar.addWidget(self.toolbar_widget3)


    def create_stacked_widget(self):
        self.stack = QStackedWidget(self)

        self.settings_widget = SettingsWidget(self.settings)
        self.running_servers_widget = RunningServersWidget()
        self.servers_widget = ServersWidget(self)

        # Create widgets for stack
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.addWidget(self.settings_widget)

        servers_widget = QWidget()
        servers_layout = QVBoxLayout(servers_widget)
        servers_layout.addWidget(self.servers_widget)

        running_servers_widget = QWidget()
        running_servers_layout = QVBoxLayout(running_servers_widget)
        running_servers_layout.addWidget(self.running_servers_widget)

        # Add widgets to stack
        self.stack.addWidget(settings_widget)
        self.stack.addWidget(servers_widget)
        self.stack.addWidget(running_servers_widget)

        # Connect actions to stacked widget
        self.action1.triggered.connect(lambda: self.stack.setCurrentIndex(0))
        self.action2.triggered.connect(lambda: self.stack.setCurrentIndex(1))
        self.action3.triggered.connect(lambda: self.stack.setCurrentIndex(2))

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)

        self.main_layout.addWidget(self.stack)
        self.main_layout.addWidget(self.progress_bar)

        # Set stack as central widget
        self.setCentralWidget(self.main_widget)


    def closeEvent(self, event):
        loop = QEventLoop()
        self.exit_thread = threads.ExitThread(self.thread_handler)
        self.exit_thread.finished.connect(loop.quit)
        self.exit_thread.start()

        timer = QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(0)
        loop.exec_()


    def refresh_widgets(self):
        # update servers widget
        try:
            self.servers_widget.refresh()
        except AttributeError:
            pass
