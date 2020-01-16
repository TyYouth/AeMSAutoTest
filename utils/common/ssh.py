#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko
from scp import SCPClient
from time import sleep
from utils.common.log import logger
from utils.time_handler import DateTime


def to_str(bytes_or_str):
    string_value = bytes_or_str
    if isinstance(bytes_or_str, bytes):
        string_value = bytes_or_str.decode('utf-8')
    return string_value


class SSHSession(object):

    def __init__(self, host, user_name, pwd, port=22):
        self.host = host
        self.port = port
        self.user_name = user_name
        self.pwd = pwd
        self.__transport = None
        self.scp_client = None
        self.sftp_client = None

    def connect(self):
        try:
            host_port = (self.host, self.port)
            transport = paramiko.Transport(host_port)
            transport.connect(username=self.user_name, password=self.pwd)
            self.__transport = transport
            self.scp_client = SCPClient(self.__transport)
            self.sftp_client = paramiko.SFTPClient.from_transport(self.__transport)
        except paramiko.ssh_exception.SSHException:
            # the henb is not support SFTP and init transport as SCP"
            logger.warning("HeNB does NOT support sftp")
        except Exception as e:
            logger.exception(e)

    def upload_file(self, local_file, target_file_path):
        self.scp_client.put(local_file, target_file_path)

    def download_file(self, remote_file_path, target_file_path):
        self.scp_client.get(remote_file_path, target_file_path)

    def list_dir_attr(self, target_path="."):
        """
        :param target_path: path to be listed
        :return: list of files' SFTPAttributes which is extend `os.stat` object
        get value like: list_file_attr[0].st_size
        """
        list_file_attr = self.sftp_client.listdir_attr(target_path)
        return list_file_attr

    def list_dir(self, target_path="."):
        """
        :param target_path: path to be listed
        :return: list of file name
        """
        list_file_name = self.sftp_client.listdir(target_path)
        return list_file_name

    def run_cmd(self, command=None):
        ssh_session = paramiko.SSHClient()
        ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh_session._transport = self.__transport
        stdin, stdout, stderr = ssh_session.exec_command(command)
        output = to_str(stdout.read()).strip()
        error = to_str(stderr.read()).strip()
        if error:
            logger.error(error)
            return error
        else:
            # logger.debug("The result of command '{}' is:\n {}".format(command, output))
            return output

    def run_command_shell(self, *commands):
        receive = None
        channel = self.__transport.open_session()
        channel.get_pty()
        channel.invoke_shell()
        for command in commands:
            channel.send(command + '\n')
        sleep(0.5)
        if channel.recv_ready():
            receive = channel.recv(65535)
        channel.close()
        logger.debug(receive.decode('UTF-8'))

    def get_date_time(self, is_transfer=True):
        date_time = self.run_cmd("date")
        if is_transfer:
            date_time = DateTime.to_datetime_by(date_time, time_format="%a %b %d %H:%M:%S %Z %Y")
        return date_time

    def close(self):
        self.__transport.close()

    def __destroy(self):
        self.close()


if __name__ == '__main__':
    host = '172.0.13.185'
    username = 'root'
    pwd = 'casa'
    henb_ssh = SSHSession(host, username, pwd)
    henb_ssh.connect()
    henb_ssh.run_command_shell('ipsec status')
    print(henb_ssh.get_date_time(is_transfer=True))
    # henb_ssh.run_command_shell('pwd', 'echo $SHELL')
    # henb_ssh.download_file('/config/l3/femtoconfig.ini', r"E:/smallcell/versionFiles/femtoconfig.ini")
    henb_ssh.close()
