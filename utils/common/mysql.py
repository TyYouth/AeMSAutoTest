#!/usr/bin/env python
# coding=utf-8
from collections import defaultdict
import pymysql
from pymysql.err import OperationalError, ProgrammingError
from pymysql.cursors import Cursor, DictCursor, SSCursor, SSDictCursor
from utils.common.log import logger

METHOD = [Cursor, DictCursor, SSCursor, SSDictCursor]


class UnSupportCursorMethodError(Exception):
    pass


class MysqlSession(object):

    def __init__(self, host, username, pwd, db_name, cursor_method=DictCursor):
        """
        :param cursor_method: a method to define return result's type, DictCursor as default
        """
        self.cursor = None
        self.host = host
        self.db_name = db_name
        try:
            self.db = pymysql.connect(self.host, username, pwd, self.db_name)
            self.cursor_init(cursor_method)
        except OperationalError:
            logger.error(
                "can NOT connect to Mysql service on {}.{} with username({} and password({}))".format(host, db_name,
                                                                                                      username, pwd))

    def cursor_init(self, method=Cursor):
        """
        :param method: support Cursor, DictCursor, SSCursor, SSDictCursor
        """
        if method in METHOD:
            logger.debug("to init cursor as {}".format(method))
            self.cursor = self.db.cursor(method)
        else:
            raise UnSupportCursorMethodError("Un-support Cursor method to init, only support {}".format(METHOD))

    def execute_sql(self, sql_cmd, is_fetchone=True, size=None):
        result = defaultdict()
        try:
            self.cursor.execute(sql_cmd)
            if is_fetchone:
                result = self.cursor.fetchone()
            elif is_fetchone is not True:
                result = self.cursor.fetchall()
            elif (is_fetchone is not True) and (size is not None):
                result = self.cursor.fetchmany(size)
        except ProgrammingError as e:
            logger.error(e)
        except Exception as e:
            logger.error("ERROR: unable to fetch data from {}:{}".format(self.host, self.db_name))
            logger.exception(e)
        finally:
            return result

    def close(self):
        self.cursor.close()
        self.db.close()


if __name__ == "__main__":
    host = "172.0.16.120"
    username = "root"
    pwd = "casa"
    db_name = "hemsdb"
    aems_db = MysqlSession(host, username, pwd, db_name)
    aems_db.execute_sql("fdafdsa")
