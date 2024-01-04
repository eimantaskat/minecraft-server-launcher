from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox


class Popup(QMessageBox):
    def __init__(self, parent, title, message, type):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setText(message)
        self.setStandardButtons(QMessageBox.Ok)

        if type == 'info':
            self.setIcon(QMessageBox.Information)
        elif type == 'warning':
            self.setIcon(QMessageBox.Warning)
        elif type == 'error':
            self.setIcon(QMessageBox.Critical)
        else:
            raise ValueError(f'Invalid type: {type}')

        self.setWindowFlags(
            Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint
        )

        self.exec_()
