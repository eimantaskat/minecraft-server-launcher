from PyQt5.QtWidgets import QComboBox


class ComboBox(QComboBox):
	def wheelEvent(self, event):
		event.ignore()
