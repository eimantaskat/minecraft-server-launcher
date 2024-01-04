from PyQt5.QtWidgets import QComboBox, QGridLayout, QPushButton, QWidget


class ServerSelection(QWidget):
	def __init__(self, parent, servers, thread_handler, start_function, console_widget, stacked_widget):
		super().__init__()
		self.parent = parent
		self.main_window = parent.main_window

		self.servers = servers
		self.start_function = start_function
		self.server_names = [
			f"{server.server_version_name}: {server.name}" for server in servers]
		self.thread_handler = thread_handler

		# Create the layout
		self.servers_selection_layout = QGridLayout()
		self.setLayout(self.servers_selection_layout)

		# Create the combo box
		self.server_select = QComboBox()
		self.server_select.addItems(self.server_names)

		# Create the start button
		self.start_button = QPushButton("Start")
		self.start_button.clicked.connect(lambda: self.start_function(
			self.main_window, self.thread_handler, self.servers, self.server_select.currentIndex(), console_widget, stacked_widget))

		# Add the widgets to the layout
		self.servers_selection_layout.addWidget(self.server_select, 0, 0)
		self.servers_selection_layout.addWidget(self.start_button, 0, 1)

	def refresh(self, servers):
		self.servers = servers
		self.server_names = [f"{server.server_version_name}: {server.name}" for server in servers]
		self.server_select.clear()
		self.server_select.addItems(self.server_names)
