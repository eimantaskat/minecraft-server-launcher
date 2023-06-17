from PyQt5.QtWidgets import QSpinBox


class SpinBox(QSpinBox):
	def wheelEvent(self, event):
		event.ignore()
