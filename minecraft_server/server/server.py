import os

from mcstatus import JavaServer
from nbt import nbt

from minecraft_server import VersionManager
from minecraft_server.server.server_properties import get_timestamp
from minecraft_server.server.server_settings import ServerSettings


class Server:
	def __init__(self, path, server_settings: ServerSettings, server_jar):
		self.warnings = []

		self.path = path
		self.server_jar = server_jar
		self.settings = server_settings
		self.settings.load_settings()

		self.world_version_id = self.get_world_version_id()
		self.server_version_id = VersionManager.get_version_id(self.server_jar)

		self.world_version_name = self.get_world_version_name()
		self.server_version_name = VersionManager.get_version(self.server_jar)

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
		command = ["java", "-Xmx" + str(getattr(self.settings, 'Xmx', 1024)) + "M", "-Xms" + str(
			getattr(self.settings, 'Xms', 1024)) + "M", "-jar", f'"{self.server_jar}"']
		if getattr(self.settings, 'bonusChest', False):
			command.append("--bonusChest")
		if getattr(self.settings, 'eraseCache', False):
			command.append("--eraseCache")
		if getattr(self.settings, 'forceUpgrade', False):
			command.append("--forceUpgrade")
		if getattr(self.settings, 'initSettings', False):
			command.append("--initSettings")
		if getattr(self.settings, 'port', False):
			command.append("--port")
			command.append(str(self.settings.port))
		if getattr(self.settings, 'safeMode', False):
			command.append("--safeMode")
		if getattr(self.settings, 'universe', False):
			command.append("--universe")
			command.append(self.settings.universe)
		if getattr(self.settings, 'world', False):
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

	def is_online(self):
		return bool(self.get_info())
		
	def get_info(self):
		try:
			server = JavaServer.lookup(f'localhost')
			status = server.status().raw
			return status
		except: # TODO: catch specific exceptions
			return {}
