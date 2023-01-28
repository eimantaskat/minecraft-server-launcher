from .msl_thread import MslThread
from minecraft_server import downloader
from PyQt5.QtCore import pyqtSignal


class DownloadThread(MslThread):
    download_finished = pyqtSignal()

    def __init__(self, jar_version, download_location):
        super().__init__()
        self.jar_version = jar_version
        self.download_location = download_location

    def _run(self):
        downloader.download_server_jar(
            self.jar_version, self.download_location)
        self.download_finished.emit()