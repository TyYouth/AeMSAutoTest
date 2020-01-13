import json
import os
from utils.common.log import logger

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
HENB_CONFIG_PATH = os.path.join(BASE_PATH, 'config', 'henb_config.json')


class JsonReader(object):
    def __init__(self, json_file):
        try:
            if os.path.exists(json_file):
                self._json_file = json_file
        except FileNotFoundError as e:
            logger.error(e)
        self._data = None

    @property
    def data(self):
        if not self._data:
            with open(self._json_file, 'rb') as file:
                self._data = json.load(file)
        return self._data


class JsonConfig(object):
    def __init__(self, json_config=HENB_CONFIG_PATH):
        self.config = JsonReader(json_config).data

    def get(self, date_name):
        if date_name in list(self.config.keys()):
            return self.config.get(date_name)


if __name__ == '__main__':
    HeNB_config = JsonConfig().get('femtoconfig.ini')
    print(HeNB_config.get('is_use_ipv6'))
