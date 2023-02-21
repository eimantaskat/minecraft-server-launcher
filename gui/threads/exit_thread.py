from gui.threads.msl_thread import MslThread
from PyQt5.QtCore import pyqtSignal


class ExitThread(MslThread):
    finished = pyqtSignal()

    def __init__(self, thread_handler):
        super().__init__()
        self.thread_handler = thread_handler

    def _run(self):    
        self.thread_handler.stop_all_threads()
        self.finished.emit()

    def stop(self):
        self.terminate()
