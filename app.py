from PyQt5.QtWidgets import QApplication

from logger import setup_logger
from gui.mc_server import MinecraftServerLauncher

if __name__ == "__main__":
	logger = setup_logger('msl')
	logger.info('Starting Minecraft Server Launcher')
	app = QApplication([])
	msl = MinecraftServerLauncher()
	msl.show()
	app.exec_()
	logger.info('Process finished cleanly')
