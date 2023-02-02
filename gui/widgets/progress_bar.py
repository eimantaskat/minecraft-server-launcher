from PyQt5.QtWidgets import QWidget, QProgressBar, QVBoxLayout, QLabel

class ProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress_bar_layout = QVBoxLayout(self)
        
        # self.label = QLabel("")
        # self.progress_bar_layout.addWidget(self.label)

        self.progress_bar = QProgressBar()
        self.progress_bar_layout.addWidget(self.progress_bar)
        self.reset()

    def start_loading(self):
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setValue(0)
    
    def stop_loading(self):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)

    def reset(self):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

    def set_maximum(self, maximum):
        self.progress_bar.setMaximum(maximum)

    def set_value(self, value):
        self.progress_bar.setValue(value)

    # def set_description(self, text):
    #     self.label.setText(text)

    def value(self):
        return self.progress_bar.value()
