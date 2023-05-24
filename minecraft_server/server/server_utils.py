import os
import errno
import glob
from minecraft_server.server.server_settings import ServerSettings
from minecraft_server import VersionManager
from gui.threads import ServerThread
from minecraft_server.server.server import Server


def start_server(thread_handler, servers, index, console_widget, toolbar_widget):
    print(index)
    running_servers = thread_handler.get_threads_by_class(ServerThread)
    if running_servers:
        print(running_servers[0].status)
        print(running_servers[0].info)
        return print("Server is already running!")

    console_widget.clear()
    selected_server = servers[index]
    server_thread = ServerThread(selected_server)
    server_thread.console_output.connect(console_widget.write)
    # server_thread.stopped.connect(console_widget.clear)
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

    settings = ServerSettings(os.path.join(path, settings_file), version)

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
