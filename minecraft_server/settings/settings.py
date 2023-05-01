import os
import json
import errno
from PyQt5.QtCore import pyqtSignal, QObject


class Settings(QObject):
    settings_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.__file_folder = f"{os.getenv('APPDATA')}\\.minecraft-server"
        self.__full_file_path = os.path.expandvars(self.__file_folder)
        self.__settings_file = f"{self.__full_file_path}\\settings.json"

        # SETTINGS
        self._data_location = f"{self.__file_folder}\\servers"
        self._auto_start = False
        self._versions_file = f"{self.__file_folder}\\versions.json"


    @property
    def versions_file(self):
        return self._versions_file


    @property
    def data_location(self):
        return os.path.expandvars(self._data_location)


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

        data = {key: value for key, value in vars(
            self).items() if not key.startswith('_Settings')}

        # with open('minecraft_server/settings/default_settings.json', 'w') as file:
        with open(self.__settings_file, 'w') as file:
            json.dump(data, file)
        self.settings_changed.emit()


    def get_default_settings(self):
        with open("minecraft_server\settings\default_settings.json", 'r') as file:
            return json.load(file)


    def load_default_settings(self):
        default_settings = self.get_default_settings()
        self.__dict__.update(default_settings)
        self.save_settings()


    def load_settings(self):
        self.create_dir()

        with open(self.__settings_file, 'r') as file:
            self.__dict__.update(json.load(file))

        self.settings_changed.emit()


    def create_dir(self):
        try:
            os.makedirs(self.__full_file_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        if not os.path.exists(self.__settings_file):
            # create the file
            open(self.__settings_file, 'w').close()
            self.load_default_settings()
