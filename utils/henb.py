#!/usr/bin/env python
# coding=utf-8
from collections import defaultdict
from utils.log import logger
from utils.ssh import SSHSession
from utils.config import Config


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
        self.device_info = defaultdict()

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

    # sed -n "/^\s*use_ipv6\s*=/p" /config/l3/femtoconfig.ini
    # \s* 匹配空格 \s* is for match space
    def get_config(self, config_name, target_file_path):
        command = 'sed -n "/^\s*{0}\s*=/p" {1}'.format(config_name, target_file_path)
        logger.debug("try to get HeNB's config by command: {}".format(command))
        respond = self.run_cmd(command)
        result = respond.split("=", 1)
        if result[0].strip() == config_name:
            logger.debug("The {} in {} is {}".format(config_name, target_file_path, result[1]))
            return result[1].strip()
        else:
            logger.error("Failed to get {} in {}, the respond is {}".format(config_name, target_file_path, respond))
            return False

    # sed -i "/^\s*use_ipv6\s*=/c use_ipv6 = 0" /config/l3/femtoconfig.ini
    def set_config(self, config_name, config_param, target_file_path):
        set_command = 'sed -i "/^\s*{0}\s*=/c {0} = {1}" {2}'.format(config_name, config_param, target_file_path)
        self.run_cmd(set_command)
        actual_result = self.get_config(config_name, target_file_path)
        if actual_result == config_param:
            logger.debug("Success to set config")
            return True
        else:
            logger.error("fail to set {} in {} as {}".format(config_name, target_file_path, config_param))
            return False

    def get_serial_number(self):
        # is file /root/.vendor/serialnumber' exist
        # is_file_exist = False
        respond = self.run_cmd('ls /root/.vendor/serialnumber')
        if "No such file or directory" in respond:
            logger.warn("file /root/.vendor/serialnumber does NOT exist")
            self.device_info['SerialNumber'] = self.get_config('DeviceInfo.SerialNumber', self.tr069_file)
        else:
            cat_command = 'cat /root/.vendor/serialnumber'
            self.device_info['SerialNumber'] = self.run_cmd(cat_command)

    def get_device_info(self):
        self.device_info['Manufacturer'] = self.get_config('DeviceInfo.Manufacturer', self.tr069_file)
        self.device_info['ManufacturerOUI'] = self.get_config('DeviceInfo.ManufacturerOUI', self.tr069_file)
        self.device_info['ProductClass'] = self.get_config('DeviceInfo.ProductClass', self.tr069_file)
        self.get_serial_number()

    def update_tr069_url(self):
        southbound_ip_address = Config().get('AeMS').get('southbound_ip_address')
        # 判断是v4 or v6(应该换个更好的方法)
        url = result = None
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

    def reboot(self):
        self.run_command_shell('reboot')


if __name__ == "__main__":
    henb = HeNB()
    # henb.run_cmd('echo $PATH')
    henb.reboot()
    henb.close()
    # henb.get_parameter_by_oam("SIB1.SIB1.TAC")
    # henb.set_parameter_by_oam("SIB1.SIB1.TAC", 4369)
    # henb.get_parameter_by_oam("SIB1.SIB1.TAC")
    # config = henb.get_config('ManagementServer.URLkjhfkj', '/config/tr069/tr069_agent.ini')
    # henb.set_config('ManagementServer.URL', "http://[172:0:17::99]:8080/hems-web-ui/ws/cwmp/",
    #                 '/config/tr069/tr069_agent.ini')
    # henb.get_module_info()
    # print(henb.device_info['ProductClass'])
    # henb.update_tr069_url()
    # henb.get_device_info()
    # print(henb.device_info)
