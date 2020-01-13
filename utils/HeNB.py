#!/usr/bin/env python
# coding=utf-8
import os
from collections import defaultdict
from utils.common.log import logger
from utils.common.ssh import SSHSession
from utils.Config import Config
from utils.Config import COMMON_FILE
from utils.CSVHandler import CsvReader
from utils.JsonFileHandler import JsonConfig

ALARM_FILE = os.path.join(COMMON_FILE, 'Alarm', 'AlarmDefinition_20190114_sxh.csv')
VALUE_CHANGE = os.path.join(COMMON_FILE, 'common', 'TR069Packet', '4_value_change.xml')


class NoSuchDeviceAlarm(Exception):
    logger.exception("No such a Device Alarm")


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

    def get_parameter_by_oam(self, param_name):
        command = "echo {0}.get | {1}".format(param_name, self.oam_file_path)
        respond = self.run_cmd(command)
        result = respond.split(" ")
        if result[0] == '0':
            logger.debug("the value of {} is {}".format(param_name, result[1]))
            return result[1].strip()
        else:
            logger.error("Failed to get parameter {} by oam command, the respond is {}".format(param_name, respond))
            return False

    def set_parameter_by_oam(self, param_name, param_val):
        set_command = "echo {0}.set {1} | {2}".format(param_name, param_val, self.oam_file_path)
        self.run_cmd(set_command)
        apply_config = "echo l3.apply_config | {}".format(self.oam_file_path)
        set_respond = self.run_cmd(apply_config)
        get_respond = self.get_parameter_by_oam(param_name)
        if set_respond == 0 and get_respond:
            return True

    def get_config(self, config_name, target_file_path, split_by="="):
        """
        sed, linux command base on Regular
        \s to match one space, \s* is for match unknown len space, /^ is for match start with
        sed -n "/^\s*use_ipv6\s*=/p" /config/l3/femtoconfig.ini

        :param config_name:
        :param target_file_path:
        :param split_by:
        :return:
        """
        command = r'sed -n "/^\s*{0}\s*{2}/p" {1}'.format(config_name, target_file_path, split_by)
        logger.debug("try to get HeNB's config by command: {}".format(command))
        respond = self.run_cmd(command)
        _config_name, _config_value = respond.split(split_by)
        # rstrip(".*") to dismiss .* 任意匹配符
        if config_name.rstrip(".*") in _config_name:
            logger.debug("The value of {} in {} is {}".format(config_name, target_file_path, _config_value))
            return _config_name.strip(), _config_value.strip()
        else:
            logger.error("Failed to get {} in {}, the respond is {}".format(config_name, target_file_path, respond))
            return False

    def set_config(self, config_name: str, config_value: str, target_file_path: str, split_by="="):
        """
        sed -i "/^\s*use_ipv6\s*=/c \use_ipv6=0" /config/l3/femtoconfig.ini
        replace content startswith \, like \use_ipv6

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
        latitude_name, current_latitude = self.get_config(config_name="FAP.GPS.LockedLatitude;INT;.*",
                                                          target_file_path=gps_config_file,
                                                          split_by=";;")
        longitude_name, current_longitude = self.get_config(config_name="FAP.GPS.LockedLongitude;INT;.*",
                                                            target_file_path=gps_config_file,
                                                            split_by=";;")
        self.set_config(config_name=latitude_name.replace("OAM", "DM"), config_value=str(latitude),
                        target_file_path=gps_config_file,
                        split_by=';;')
        self.set_config(config_name=longitude_name.replace("OAM", "DM"), config_value=str(longitude),
                        target_file_path=gps_config_file,
                        split_by=';;')
        current_scan_status = self.get_config(config_name="FAP.GPS.ScanStatus;STRING;.*",
                                              target_file_path=gps_config_file,
                                              split_by=";;")[0]

        if (latitude != '0') and (longitude != '0'):
            self.set_config(config_name=current_scan_status.replace("OAM", "DM"), config_value="Success",
                            target_file_path=gps_config_file, split_by=";;")
        else:
            self.set_config(config_name=current_scan_status.replace("OAM", "DM"), config_value="Indeterminate",
                            target_file_path=gps_config_file, split_by=";;")

    @staticmethod
    def parse_alarm_definition(alarm_id):
        csv_reader = CsvReader(ALARM_FILE)
        csv_reader.close_file()
        if alarm_id in csv_reader.file_info.keys():
            if alarm_id.startswith('1'):
                logger.warning("The alarm id start with 1 is AeMS's alarm")
            alarm_dict = csv_reader.get_by_id_index(alarm_id)
            return alarm_dict
        else:
            logger.exception(NoSuchDeviceAlarm)


if __name__ == "__main__":
    henb = HeNB()

    # henb.get_parameter_by_oam("SIB1.SIB1.TAC")
    # henb.set_parameter_by_oam("SIB1.SIB1.TAC", 4369)
    henb.get_parameter_by_oam("SIB1.SIB1.TAC")

    # config = henb.get_config('ManagementServer.Manufacturer', '/config/tr069/tr069_agent.ini')

    # henb.get_device_info()
    # print(henb.device_info['ProductClass'])
    henb.update_gps("42691842", "-71203095")
    henb.get_device_info()
    print(henb.device_info)
    print(henb.device_info['Manufacturer'])
    henb.update_tr069_url()
    # henb.reboot()
    # henb.close()
