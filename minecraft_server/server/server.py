import os
from nbt import nbt
from minecraft_server.server.server_settings import ServerSettings
from minecraft_server.version import get_version, get_version_id
from minecraft_server.server_properties import get_timestamp


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

        if os.path.exists(world_folder):
            return world_folder
        return None


    def get_world_version_id(self):
        world_folder = self.get_world_folder()
        if not world_folder:
            return None

        level_dat = nbt.NBTFile(os.path.join(world_folder, 'level.dat'), 'rb')
        world_version_id = level_dat['Data']['Version']['Id'].value

        return world_version_id


    def get_world_version_name(self):
        world_folder = self.get_world_folder()
        if not world_folder:
            return None

        level_dat = nbt.NBTFile(os.path.join(world_folder, 'level.dat'), 'rb')
        world_version_id = level_dat['Data']['Version']['Name'].value

        return world_version_id


    def _verify_versions(self):
        if self.world_version_id != self.server_version_id:
            self.warnings.append(f"Server and world versions do not match: server version \
            {self.server_version_name}, world version {self.world_version_name}")


    def get_run_command(self):
        command = ["java", "-Xmx" + str(self.settings.Xmx) + "M", "-Xms" + str(
            self.settings.Xms) + "M", "-jar", self.server_jar]
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

    def agree_to_eula(self):
        comments = ["#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).\n"]
        comments.append(f"#{get_timestamp()}\n")

        eula_path = os.path.join(self.path, 'eula.txt')
        with open(eula_path, 'w') as f:
            for comment in comments:
                f.write(comment)
            f.write('eula=true')
