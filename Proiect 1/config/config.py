import configparser
import os


class ConfigManager:
    def __init__(self):
        dir = os.path.dirname(__file__)
        self.config_file = os.path.join(dir, 'settings.ini')
        self.parser = configparser.ConfigParser()
        self.parser.read(self.config_file)

    def get_default(self, key):
        try:
            return self.parser.get('DEFAULT', key)
        except Exception as e:
            print(e)
            return None

    def set_default(self, key, value):
        try:
            return self.parser.set('DEFAULT', key, value)
        except Exception as e:
            print(e)
            return None
