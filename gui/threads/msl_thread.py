from PyQt5.QtCore import QThread, pyqtSignal
import sys
import traceback


class MslThread(QThread):
    exception_raised = pyqtSignal(Exception, str)


    def run(self):
        try:
            self._run()
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()

            msg = "".join(traceback.format_exception(
                exc_type, exc_value, exc_traceback))
            self.exception_raised.emit(e, msg)


    def _run(self):
        raise NotImplementedError("You must implement _run method")
