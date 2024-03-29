import errno
import glob
import logging
import os

from gui.threads.server_thread import ServerThread
from gui.widgets.popup_widget import Popup
from minecraft_server.server.server import Server
from minecraft_server.server.server_settings import ServerSettings
from minecraft_server.version_manager import VersionManager

logger = logging.getLogger('msl')


def start_server_from_list(main_window, thread_handler, servers, index, console_widget, toolbar_widget):
	server = servers[index]
	start_server(main_window, thread_handler, server, console_widget, toolbar_widget)


def start_server(main_window, thread_handler, server, console_widget, toolbar_widget):
	running_servers = thread_handler.get_threads_by_class(ServerThread)
	if running_servers:
		logger.warning("Server is already running")
		return
	
	def create_popup(title, message, icon):
		Popup(main_window, title, message, icon)

	console_widget.clear()
	server_thread = ServerThread(server)
	server_thread.console_output.connect(console_widget.write)
	server_thread.help_output.connect(console_widget.set_available_commands)
	server_thread.popup.connect(create_popup)
	console_widget.input_signal.connect(server_thread.send_command)
	thread_handler.start_thread(server_thread)
	toolbar_widget.mousePressEvent(None)


def load_server(path):
	settings_file = 'server.settings'
	jar_pattern = '*.jar'

	jar_files = glob.glob(os.path.join(path, jar_pattern))

	versions = []
	for file in jar_files:
		try:
			version = VersionManager.get_version_id(file)
			versions.append(version)
		except KeyError:
			pass
	if not versions:
		return  # No server file found
	elif len(versions) == 1:
		version, = versions
	else:
		# TODO raise custom error
		raise Exception(f"Found {len(versions)} *.jar files")

	settings = ServerSettings(settings_file=os.path.join(path, settings_file), version=version)

	server = Server(path, settings, jar_files[0])

	return server


def get_servers(data_location):
	data_location = os.path.expandvars(data_location)
	try:
		os.makedirs(data_location)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise

	servers_folders = [f for f in os.listdir(
		data_location) if os.path.isdir(os.path.join(data_location, f))]

	servers = []
	for servers_folder in servers_folders:
		server = load_server(os.path.join(data_location, servers_folder))
		servers.append(server)

	servers = [server for server in servers if server is not None]
	return servers
