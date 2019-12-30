#!/usr/bin/env python
# coding=utf-8
from collections import defaultdict
from utils.common.log import logger
from utils.config import Config
from utils.common.mysql import MysqlSession

db_config = Config().get("AeMS").get("mysql")


class HemsDB(MysqlSession):

    def __init__(self):
        self.host = db_config.get("host")
        self.username = db_config.get("username") if db_config.get("username") else "root"
        self.pwd = db_config.get("password") if db_config.get("password") else "casa"
        self.db_name = db_config.get("db_name") if db_config.get("db_name") else "hemsdb"
        super().__init__(self.host, self.username, self.pwd, self.db_name)
        self.db_data = defaultdict()

    def get_cm_start_time(self):
        # 'cmStartTime': datetime.datetime(2019, 12, 17, 20, 0)
        sql_command = "select cmStartTime from inventorydump where id = 1"
        cm_start_time = self.execute_sql(sql_command)['cmStartTime']
        return cm_start_time


if __name__ == "__main__":
    hemsdb = HemsDB()
    print(hemsdb.get_cm_start_time())
