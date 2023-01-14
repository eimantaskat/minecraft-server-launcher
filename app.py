from PyQt5.QtWidgets import QApplication
from gui.mc_server import MinecraftServerLauncher

if __name__ == "__main__":
    app = QApplication([])
    downloader = MinecraftServerLauncher()
    downloader.show()
    app.exec_()
