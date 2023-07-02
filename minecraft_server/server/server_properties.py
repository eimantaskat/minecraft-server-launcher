import os
from minecraft_server.utils import get_timestamp


class ServerProperties:
	def __init__(self, server_path=None, properties=None):
		self._properties = None
		if server_path is None:
			self._server_path = None
			self.properties_path = None
		else:
			self.server_path = server_path

		if properties is not None:
			self.properties = properties
		elif self.properties is None:
			self.read_default_server_properties()

	@property
	def server_path(self):
		return self._server_path
	
	@server_path.setter
	def server_path(self, server_path):
		self._server_path = os.path.abspath(server_path)
		self.properties_path = os.path.join(self._server_path, 'server.properties')
		self.read()

	@property
	def properties(self):
		return self._properties

	@properties.setter
	def properties(self, properties):
		self._properties = {}
		for key, value in properties.items():
			if key != 'motd':
				self._properties[key] = str(value).lower()
			else:
				self._properties[key] = str(value)


	def read(self, properies_path=None):
		if properies_path is None:
			properies_path = self.properties_path

		if not os.path.exists(properies_path):
			return self.read_default_server_properties()

		self._properties = {}
		with open(properies_path, 'r') as f:
			for line in f:
				if not line.startswith('#'):
					key, value = line.strip().split('=')
					self._properties[key] = value

		self._unstringify_values()
	
	def write(self):
		properties = {}
		comments = []
		with open(self.properties_path, 'r') as f:
			for line in f:
				if line.startswith('#'):
					if "#" in line and ":" in line:
						comments.append(f"#{get_timestamp()}\n")
					else:
						comments.append(line)
				else:
					key, value = line.strip().split('=')
					properties[key] = value

		for key, value in self._properties.items():
			properties[key] = value

		with open(self.properties_path, 'w') as f:
			for comment in comments:
				f.write(comment)
			for key, value in properties.items():
				f.write(key + '=' + value + '\n')

	def _unstringify_values(self):
		for key, value in self._properties.items():
			if key != 'motd':
				if isinstance(value, bool):
					self._properties[key] = value
				elif isinstance(value, str) and value.lower() == 'true':
					self._properties[key] = True
				elif isinstance(value, str) and value.lower() == 'false':
					self._properties[key] = False
				else:
					try:
						self._properties[key] = int(value)
					except ValueError:
						try:
							self._properties[key] = float(value)
						except ValueError:
							self._properties[key] = value
			else:
				self._properties[key] = value

		self._properties['gamemode'] = self._properties['gamemode'].capitalize()
		self._properties['difficulty'] = self._properties['difficulty'].capitalize()

	def create(self):
		comments = ["#Minecraft server properties\n"]
		comments.append(f"#{get_timestamp()}\n")
		with open(self.properties_path, 'w') as f:
			for comment in comments:
				f.write(comment)
			for key, value in self._properties.items():
				f.write(key + '=' + value + '\n')

	def read_default_server_properties(self):
		path = os.path.abspath('./minecraft_server/settings/server.properties')
		self.read(properies_path=path)