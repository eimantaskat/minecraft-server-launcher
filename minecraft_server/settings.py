import os
import json
import errno


class Settings:
    def __init__(self):
        self.__file_folder = f"{os.getenv('APPDATA')}\.minecraft-server"
        self.__settings_file = f"{self.__file_folder}\settings.json"

        # SETTINGS
        self._data_location = f"{self.__file_folder}\servers"
        self._auto_start = False

    @property
    def data_location(self):
        return self._data_location

    @data_location.setter
    def data_location(self, value):
        self._data_location = value
        self.save_settings()

    @property
    def auto_start(self):
        return self._auto_start

    @auto_start.setter
    def auto_start(self, value):
        self._auto_start = value
        self.save_settings()

    def save_settings(self):
        self.create_dir()

        data = {key: value for key, value in vars(self).items() if not key.startswith('_Settings')}

        # with open('minecraft_server/default_settings.json', 'w') as file:
        with open(self.__settings_file, 'w') as file:
            json.dump(data, file)


    def get_default_settings(self):
        with open("minecraft_server\default_settings.json", 'r') as file:
            return json.load(file)

    def load_default_settings(self):
        default_settings = self.get_default_settings()
        self.__dict__.update(default_settings)
        self.save_settings()

    def load_settings(self):
        self.create_dir()
        
        with open(self.__settings_file, 'r') as file:
            self.__dict__.update(json.load(file))

    def create_dir(self):
        try:
            os.makedirs(self.__file_folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        if not os.path.exists(self.__settings_file):
            # create the file
            open(self.__settings_file, 'w').close()
            self.load_default_settings()
