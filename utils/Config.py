import os
import yaml


# get current file's father folder's abspath
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_PATH = os.path.join(BASE_PATH, 'config', 'config.yml')
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
CASE_PATH = os.path.join(BASE_PATH, 'test', 'case')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')
REPORT_FILE = os.path.join(REPORT_PATH, 'report.html')
DATA_PATH = os.path.join(BASE_PATH, 'data')
COMMON_FILE = os.path.join(DATA_PATH, 'common')


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


if __name__ == '__main__':
    config_var = Config().get('HeNB')
    print(config_var.get('host'))
