from PyQt5 import QtWidgets, QtGui
from minecraft_server import version
from . import threads


class MinecraftServerLauncher(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.thread_handler = threads.ThreadHandler()
        # Create the UI elements
        self.jar_version_label = QtWidgets.QLabel("Select version:")
        self.jar_version_combo = QtWidgets.QComboBox()
        self.download_location_label = QtWidgets.QLabel("Download location:")
        self.download_location_edit = QtWidgets.QLineEdit("./server_versions")
        self.download_button = QtWidgets.QPushButton("Download")

        # Create the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.jar_version_label)
        layout.addWidget(self.jar_version_combo)

        # Create Settings menu
        settings_group_box = QtWidgets.QGroupBox("Settings")
        settings_layout = QtWidgets.QFormLayout()
        settings_layout.addRow(self.download_location_label,
                            self.download_location_edit)
        settings_group_box.setLayout(settings_layout)
        layout.addWidget(settings_group_box)

        layout.addWidget(self.download_button)
        self.setLayout(layout)

        # Connect the download button to the download function
        self.download_button.clicked.connect(self._download_handler)

        # Populate the version_combo with available versions
        self.jar_version_combo.addItems(version.get_minecraft_versions())

        # Set the window properties
        self.setWindowTitle("Minecraft Server Launcher")
        self.setWindowIcon(QtGui.QIcon("icon.png"))


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
