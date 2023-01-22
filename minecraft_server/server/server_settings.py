import os
import json


class ServerSettings:
    def __init__(self, settings_file='', version=None) -> None:
        self.__settings_file = settings_file
        self.__version = version
        
        # SETTINGS
        self._Xmx = 2048                # Maximum heap memory size
        self._Xms = 2048                # Initial heap memory size
        self._bonusChest = False        # If a bonus chest should be generated, when the world is first generated
        self._eraseCache = False        # Erases the lighting caches, etc.
        self._forceUpgrade = False      # Forces upgrade on all the chunks
        self._initSettings = False      # Loads the settings from 'server.properties' and 'eula.txt', then quits
        self._port = 25565              # Which port to listen on, overrides the server.properties value
        self._safeMode = False          # Loads level with vanilla datapack only.
        self._universe = '.'            # The folder in which to look for world folders
        self._world = 'world'           # The name of the world folder in which the level.dat resides

    def save_settings(self):
        if not self.__settings_file:
            return

        self.create_settings_file()

        data = {key: value for key, value in vars(self).items() if not key.startswith('_ServerSettings')}

        # with open('minecraft_server/default_settings.json', 'w') as file:
        with open(self.__settings_file, 'w') as file:
            json.dump(data, file)

    def load_default_settings(self):
        default_settings = get_default_settings()
        self.__dict__.update(default_settings)
        self.save_settings()

    def load_settings(self):
        if not self.__settings_file:
            return
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

    @property
    def Xmx(self):
        """Maximum heap memory size"""
        return self._Xmx
    
    @Xmx.setter
    def Xmx(self, value):
        self._Xmx = value
        self.save_settings()
        
    @property
    def Xms(self):
        """Initial heap memory size"""
        return self._Xms
    
    @Xms.setter
    def Xms(self, value):
        self._Xms = value
        self.save_settings()
        
    @property
    def bonusChest(self):
        """Generate bonus chest on first start"""
        return self._bonusChest
    
    @bonusChest.setter
    def bonusChest(self, value):
        self._bonusChest = value
        self.save_settings()
        
    @property
    def eraseCache(self):
        """Erase the cache before starting the server"""
        return self._eraseCache
    
    @eraseCache.setter
    def eraseCache(self, value):
        self._eraseCache = value
        self.save_settings()
        
    @property
    def forceUpgrade(self):
        """Force an upgrade of the server"""
        return self._forceUpgrade
    
    @forceUpgrade.setter
    def forceUpgrade(self, value):
        self._forceUpgrade = value
        self.save_settings()
        
    @property
    def initSettings(self):
        """Initialize the settings and quit"""
        return self._initSettings
    
    @initSettings.setter
    def initSettings(self, value):
        self._initSettings = value
        self.save_settings()
        
    @property
    def port(self):
        """Server port number"""
        return self._port
    
    @port.setter
    def port(self, value):
        self._port = value
        self.save_settings()
        
    @property
    def safeMode(self):
        """Load level with vanilla datapack only"""
        return self._safeMode
    
    @safeMode.setter
    def safeMode(self, value):
        self._safeMode = value
        self.save_settings()
        
    @property
    def universe(self):
        """The folder in which to look for world folders"""
        return self._universe
    
    @universe.setter
    def universe(self, value):
        self._universe = value
        self.save_settings()
    
    @property
    def world(self):
        """Name of the world"""
        return self._world

    @world.setter
    def world(self, value):
        self._world = value
        self.save_settings()
 
def get_default_settings():
    with open("minecraft_server\settings\default_server_settings.json", 'r') as file:
        return json.load(file)