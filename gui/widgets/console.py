from PyQt5.QtWidgets import QWidget, QTextEdit, QLineEdit, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui

class ConsoleWidget(QWidget):
    input_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Create a QTextEdit widget for the console
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(100)
        # self.console.setStyleSheet("border: 0px;")

        self.input = QLineEdit(self)
        self.input.returnPressed.connect(self._write_to_console)

        # Create a layout for the widget
        layout = QVBoxLayout()
        layout.addWidget(self.console)
        layout.addWidget(self.input)
        layout.setSpacing(0)
        self.setLayout(layout)


    def write(self, text):
        cursor = self.console.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.console.setTextCursor(cursor)
        self.console.insertPlainText(text)
        self.console.verticalScrollBar().setValue(self.console.verticalScrollBar().maximum())



    def _write_to_console(self):
        text = self.input.text()
        # A method to write a message to the console
        self.input_signal.emit(text)
        self.write(f"{text}\n")
        self.input.clear()


    def clear(self):
        self.console.clear()
        self.input.clear()
