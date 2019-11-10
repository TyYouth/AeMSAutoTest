import os
import yaml
import json

# get current file's father folder's abspath
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_PATH = os.path.join(BASE_PATH, 'config', 'config.yml')
HENB_CONFIG_PATH = os.path.join(BASE_PATH, 'config', 'henb_config.json')
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
CASE_PATH = os.path.join(BASE_PATH, 'test', 'case')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')
REPORT_FILE = os.path.join(REPORT_PATH, 'report.html')
DATA_FILE = os.path.join(BASE_PATH, 'data')


class YamlReader(object):
    def __init__(self, yaml_file):
        try:
            # check whether yml file is exists or not
            if os.path.exists(yaml_file):
                self.yaml_file = yaml_file
        except FileNotFoundError:
            print('File was not found')
        self._data = None

    @property
    def data(self):
        # if opening yml first time, load it as a list type variable
        if not self._data:
            with open(self.yaml_file, 'rb') as file:
                self._data = list(yaml.safe_load_all(file))
        return self._data


class Config(object):
    def __init__(self, config=CONFIG_PATH):
        self.config = YamlReader(config).data

    """
    yaml set file parts based on '---', and retrun a list type variable
    get(): return 1st part and get diff by change index value
    configuring framework's default configuration in 1st part
    """

    def get(self, element, index=0):
        return self.config[index].get(element)


class JsonReader(object):
    def __init__(self, jsonfile):
        try:
            if os.path.exists(jsonfile):
                self.jsonfile = jsonfile
        except FileNotFoundError as e:
            raise e
        self._data = None

    @property
    def data(self):
        if not self._data:
            with open(self.jsonfile, 'rb') as file:
                self._data = json.load(file)
        return self._data


class JsonConfig(object):
    def __init__(self, jsonc_onfig=HENB_CONFIG_PATH):
        self.config = JsonReader(jsonc_onfig).data

    def get(self, date_name):
        try:
            if date_name in list(self.config.keys()):
                return self.config.get(date_name)
        except:
            print('not such henb file or config')


if __name__ == '__main__':
    config_var = Config().get('HeNB')
    print(config_var.get('host'))
    # json_config = JsonConfig().get('femtoconfig.ini')
    # print(json_config.get('is_use_ipv6'))
