import json
import os


class ServerSettings:
	def __init__(self, settings_file='', version=None) -> None:
		self.__settings_file = settings_file
		self.__version = version
		self.__config_file = 'default_server_config.json'

		self.load_settings()

	def __setattr__(self, name, value):
		if name.startswith('_ServerSettings'):
			self.__dict__[name] = value
			return
		self.__dict__[name] = value
		self.save_settings()

	# def __getattr__(self, name):
	#     default_settings = self.get_default_settings()
	#     if name in default_settings:
	#         self.__dict__[name] = default_settings[name]
	#         self.save_settings()
	#         return default_settings[name]
	#     else:
	#         raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

	def get_default_settings(self):
		with open(self.__config_file, 'r') as file:
			config = json.load(file)
			settings_config = config['settings']

		default_settings = {}
		for setting in settings_config:
			setting_key = setting['key']
			setting_value = setting['default_value']
			default_settings[setting_key] = setting_value

		return default_settings

	def save_settings(self):
		if not self.__settings_file:
			return

		self.create_settings_file()

		data = {key: value for key, value in vars(
			self).items() if not key.startswith('_ServerSettings')}

		# with open('minecraft_server/default_settings.json', 'w') as file:
		with open(self.__settings_file, 'w') as file:
			json.dump(data, file)

	def __init_default_settings(self):
		default_settings = self.get_default_settings()
		self.__dict__.update(default_settings)

	def load_default_settings(self):
		default_settings = self.get_default_settings()
		self.__dict__.update(default_settings)
		self.save_settings()

	def load_settings(self):
		if not self.__settings_file:
			return self.__init_default_settings()
		self.create_settings_file()

		with open(self.__settings_file, 'r') as file:
			self.__dict__.update(json.load(file))

	def create_settings_file(self):
		if not os.path.exists(self.__settings_file):
			# TODO create alert that settings file does not exist
			# create the file
			open(self.__settings_file, 'w').close()
			self.load_default_settings()

	@property
	def version(self):
		return self.__version
