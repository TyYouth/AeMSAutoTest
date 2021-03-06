#!/usr/bin/env python
# coding=utf-8
import os
from collections import defaultdict
from utils.common.log import logger
from utils.common.ssh import SSHSession
from utils.config import Config
from utils.config import COMMON_FILE
from utils.csv_handler import CsvReader
from utils.json_file_handler import JsonConfig

ALARM_FILE = os.path.join(COMMON_FILE, 'Alarm', 'AlarmDefinition_20190114_sxh.csv')
VALUE_CHANGE = os.path.join(COMMON_FILE, 'common', 'TR069Packet', '4_value_change.xml')


class NoSuchDeviceAlarm(Exception):
    pass


class HeNB(SSHSession):
    def __init__(self):
        super(SSHSession, self).__init__()
        self.config = Config().get('HeNB')
        if self.config:
            self.host = self.config.get('host')
            self.port = self.config.get('port') if self.config.get('port') else 22
            self.user_name = self.config.get('user_name') if self.config.get('user_name') else 'root'
            self.pwd = self.config.get('password') if self.config.get('password') else 'Ca$a@pex!234'
            self.oam_file_path = self.config.get('oam_file') if self.config.get(
                'oam_file') else '/usr/sbin/oam'
            self.tr069_file = self.config.get('TR069_file') if self.config.get(
                'TR069_file') else '/config/tr069/tr069_agent.ini'
        self.connect()
        self.device_info = defaultdict(dict)

    def get_parameter_by_oam(self, param_name: str):
        get_command = "echo {0}.get | {1}".format(param_name, self.oam_file_path)
        respond = self.run_cmd(get_command)
        result = respond.split(" ")
        if result[0] == '0':
            logger.debug("the value of {} is {}".format(param_name, result[1]))
            return result[1].strip()
        else:
            logger.error("Failed to get parameter {} by oam command, the respond is {}".format(param_name, respond))
            return False

    def set_parameter_by_oam(self, param_name: str, param_val):
        set_command = "echo {0}.set {1} | {2}".format(param_name, param_val, self.oam_file_path)
        self.run_cmd(set_command)
        apply_config = "echo l3.apply_config | {}".format(self.oam_file_path)
        set_respond = self.run_cmd(apply_config)
        get_respond = self.get_parameter_by_oam(param_name)
        if set_respond == 0 and get_respond:
            return True

    # sed, linux command base on Regular
    # \s to match one space, \s* is for match unknown len space, /^ is for match start with
    # sed -n "/^\s*use_ipv6\s*=/p" /config/l3/femtoconfig.ini
    def get_config(self, config_name, target_file_path, split_by="="):
        """
        :param config_name:
        :param target_file_path:
        :param split_by:
        :return:
        """
        get_command = r'sed -n "/^\s*{0}\s*{2}/p" {1}'.format(config_name, target_file_path, split_by)
        # logger.debug("try to get HeNB's config by command: {}".format(command))
        respond = self.run_cmd(get_command)
        _config_name, _config_value = respond.split(split_by)
        if config_name in _config_name:
            logger.debug("The value of {} in {} is {}".format(config_name, target_file_path, _config_value))
            return _config_name.strip(), _config_value.strip()
        else:
            logger.error("Failed to get {} in {}, the respond is {}".format(config_name, target_file_path, respond))
            return False

    # sed -i "/^\s*use_ipv6\s*=/c \use_ipv6=0" /config/l3/femtoconfig.ini  to replace content
    # startswith \, like \use_ipv6
    def set_config(self, config_name: str, config_value: str, target_file_path: str, split_by="="):
        """
        :param config_name:
        :param config_value: value you want to set
        :param target_file_path: path of config
        :param split_by:
        :return: the result of config set
        """
        set_command = r'sed -i "/^\s*{0}\s*{3}/c \{0}{3}{1}" {2}'.format(config_name, config_value, target_file_path,
                                                                         split_by)
        self.run_cmd(set_command)
        actual_name, actual_value = self.get_config(config_name, target_file_path, split_by=split_by)
        if actual_value == config_value:
            logger.debug("Success to set config")
            return True
        else:
            logger.error("fail to set {} in {} as {}".format(config_name, target_file_path, config_value))
            return False

    def get_serial_number(self):
        respond = self.run_cmd('ls /root/.vendor/serialnumber')
        if "No such file or directory" in respond:
            logger.warning("file /root/.vendor/serialnumber does NOT exist")
            serial_number = self.get_config('DeviceInfo.SerialNumber', self.tr069_file)[1]
        else:
            cat_command = 'cat /root/.vendor/serialnumber'
            serial_number = self.run_cmd(cat_command)
        return serial_number

    def get_device_info(self):
        # vendor is equals to Manufacturer
        self.device_info['Vendor'] = self.get_config('DeviceInfo.Manufacturer', self.tr069_file)[1]
        self.device_info['OUI'] = self.get_config('DeviceInfo.ManufacturerOUI', self.tr069_file)[1]
        self.device_info['ProductClass'] = self.get_config('DeviceInfo.ProductClass', self.tr069_file)[1]
        self.device_info['SerialNumber'] = self.get_serial_number()
        return self.device_info

    def update_tr069_url(self, southbound_ip_address: str = None):
        """
        to update ManagementServer.URL to AeMS southbound_ip_address
        :return: result of update
        """
        url = result = None
        if southbound_ip_address is None:
            southbound_ip_address = Config().get('AeMS').get('southbound_ip_address')
        # 判断是v4 or v6(应该换个更好的方法), re.match?
        if '.' in southbound_ip_address:
            url = "http://{0}:8080/hems-web-ui/ws/cwmp/".format(southbound_ip_address)
            result = True
        elif ':' in southbound_ip_address:
            url = "http://[{0}]:8080/hems-web-ui/ws/cwmp/".format(southbound_ip_address)
            result = True
        else:
            logger.error("incorrect southbound ip")
        if result:
            self.set_config('ManagementServer.URL', url, self.tr069_file)
            result = False
        return result

    def reboot(self):
        self.run_command_shell('reboot')

    def update_gps(self, latitude: str, longitude: str):
        gps_config_file = JsonConfig().get("parameters.csv").get("path")
        latitude_replace = r"sed -i '/FAP.GPS.LockedLatitude;INT;.*;;/c \FAP.GPS.LockedLatitude;INT;DM;R;1;0;1;0;;{}' {}"
        self.run_cmd(latitude_replace.format(latitude, gps_config_file))
        longitude_replace = r"sed -i '/FAP.GPS.LockedLongitude;INT;.*;;/c \FAP.GPS.LockedLongitude;INT;DM;R;1;0;1;0;;{}' {}"
        self.run_cmd(longitude_replace.format(longitude, gps_config_file))

        scan_status_replay = r"sed -i '/FAP.GPS.ScanStatus;INT;.*;;/c \FAP.GPS.ScanStatus;INT;DM;R;1;0;1;0;;{}'{} "
        if (latitude != '0') and (longitude != '0'):
            self.run_cmd(scan_status_replay.format("Success", gps_config_file))
        else:
            self.run_cmd(scan_status_replay.format("Indeterminate", gps_config_file))

    @staticmethod
    def parse_alarm_definition(alarm_id: str):
        csv_reader = CsvReader(ALARM_FILE)
        csv_reader.close_file()
        if alarm_id.startswith('1'):
            logger.warning("The alarm id start with 1 is AeMS's alarm")

        if alarm_id in csv_reader.file_info.keys():
            alarm_dict = csv_reader.get_by_id_index(alarm_id)
            return alarm_dict
        else:
            logger.exception("No such a device alarm {}".format(alarm_id))


if __name__ == "__main__":
    henb = HeNB()

    # henb.get_parameter_by_oam("SIB1.SIB1.TAC")
    # henb.set_parameter_by_oam("SIB1.SIB1.TAC", 4369)
    henb.get_parameter_by_oam("SIB1.SIB1.TAC")

    name, value = henb.get_config('DeviceInfo.Manufacturer', '/config/tr069/tr069_agent.ini')
    print("{} = {}".format(name, value))

    henb.update_gps("42691842", "-71203095")
    henb.get_device_info()
    print(henb.device_info)
    print(henb.device_info['Vendor'])
    henb.update_tr069_url()

    alarm = henb.parse_alarm_definition("200s1")

    # henb.reboot()
    henb.close()

