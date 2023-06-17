from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy


class FullWindowWidget(QWidget):
	def __init__(self, parent, layout):
		super().__init__()
		self.parent = parent
		self.main_window = parent.main_window

		main_layout = QVBoxLayout(self)
		main_layout.setContentsMargins(0, 0, 0, 0)
		main_layout.setSpacing(0)

		# Create header widget with close button
		header_widget = QWidget()
		header_layout = QHBoxLayout(header_widget)
		header_layout.setContentsMargins(4, 4, 4, 4)

		close_button = QPushButton("Close")
		close_button.clicked.connect(self.destroy)

		header_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
		header_layout.addWidget(close_button)

		header_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		main_layout.addWidget(header_widget)

		# Create body widget with the provided layout
		body_widget = QWidget()
		body_widget.setLayout(layout)
		main_layout.addWidget(body_widget)

	def show(self):
		self.main_window.hide_main_layout()
		self.main_window.main_widget.setParent(None)
		self.main_window.setCentralWidget(self)
		return

	def destroy(self, *args, **kwargs):
		self.setParent(None)
		self.main_window.setCentralWidget(self.main_window.main_widget)
		self.main_window.show_main_layout()
		return super().destroy(*args, **kwargs)
