import os
import json
import errno
import glob
from nbt import nbt
from .server_settings import ServerSettings
from .version import get_version, get_version_id


def load_server(path):
    settings_file = 'server_settings.json'
    jar_pattern = '*.jar'

    jar_files = glob.glob(os.path.join(path, jar_pattern))

    versions = []
    for file in jar_files:
        try:
            version = get_version(file)
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

    settings = ServerSettings(version, os.path.join(path, settings_file))

    server = Server(path, settings, jar_files[0])

    return server


def get_servers(data_location):
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


class Server:
    def __init__(self, path, server_settings: ServerSettings, server_jar):
        self.warnings = []

        self.path = path
        self.server_jar = server_jar
        self.settings = server_settings
        self.settings.load_settings()

        self.world_version_id = self.get_world_version_id()
        self.server_version_id = get_version_id(self.server_jar)

        self.world_version_name = self.get_world_version_name()
        self.server_version_name = get_version(self.server_jar)

        self._verify_versions()

        self.name = os.path.split(self.path)[-1]

    def get_world_folder(self):
        if os.path.isabs(self.settings.universe):
            universe_path = self.settings.universe
        else:
            universe_path = os.path.abspath(
                os.path.join(self.path, self.settings.universe))

        world_folder = os.path.join(universe_path, self.settings.world)
        return world_folder

    def get_world_version_id(self):
        world_folder = self.get_world_folder()

        level_dat = nbt.NBTFile(os.path.join(world_folder, 'level.dat'), 'rb')
        world_version_id = level_dat['Data']['Version']['Id'].value

        return world_version_id

    def get_world_version_name(self):
        world_folder = self.get_world_folder()

        level_dat = nbt.NBTFile(os.path.join(world_folder, 'level.dat'), 'rb')
        world_version_id = level_dat['Data']['Version']['Name'].value

        return world_version_id

    def _verify_versions(self):
        if self.world_version_id != self.server_version_id:
            self.warnings.append(f"Server and world versions do not match: server version \
            {self.server_version_name}, world version {self.world_version_name}")

    def get_run_command(self):
        command = ["java", "-Xmx" + str(self.settings.Xmx) + "M", "-Xms" + str(self.settings.Xms) + "M", "-jar", self.server_jar]
        if self.settings.bonusChest:
            command.append("--bonusChest")
        if self.settings.eraseCache:
            command.append("--eraseCache")
        if self.settings.forceUpgrade:
            command.append("--forceUpgrade")
        if self.settings.initSettings:
            command.append("--initSettings")
        if self.settings.port:
            command.append("--port")
            command.append(str(self.settings.port))
        if self.settings.safeMode:
            command.append("--safeMode")
        if self.settings.universe:
            command.append("--universe")
            command.append(self.settings.universe)
        if self.settings.world:
            command.append("--world")
            command.append(self.settings.world)

        command.append("--nogui")
        return command
