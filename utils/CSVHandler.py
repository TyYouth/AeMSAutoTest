#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
from collections import defaultdict
from utils.common.log import logger
from utils.config import COMMON_FILE

alarm_file = os.path.join(COMMON_FILE, 'Alarm', 'AlarmDefinition_20190114_sxh.csv')


class CsvReader(object):

    def __init__(self, file, has_header=True):
        if os.path.exists(file):
            self._file = open(file, 'r', newline='')
        else:
            raise FileNotFoundError("The File is NOT exist")
        self.reader = csv.reader(self._file)
        self.has_header = has_header
        self.header = self.get_header()
        self._file_info = defaultdict(dict)
        self.file_info = self.build_dict_by_id()

    def re_reader(self):
        """csv need to re-read to traversing from scratch"""
        self.reader = csv.reader(self._file)
        # 如果已经存在头部则跳过
        if self.header:
            next(self.reader)

    def get_header(self):
        # if firs row is header
        if self.has_header:
            self.header = next(self.reader)
            logger.debug("The header is {}".format(self.header))
            return self.header

    def build_dict_by_id(self):
        if not self._file_info:
            for line in self.reader:
                for row_num, info in enumerate(line):
                    # thinking first row 0 is id
                    self._file_info[line[0]][self.header[row_num]] = info
        return self._file_info

    def get_by_id_index(self, id_index):
        info_dict = self.file_info[id_index]
        logger.debug("the content of {} is: {}".format(id_index, info_dict))
        return info_dict

    def get_index_by_attr(self, attr):
        """
        :param attr: attribute of header
        :return: index of attribute
        """
        if self.header:
            index = self.header.index(attr)
            logger.debug("the index of {} is {}".format(attr, index))
            return index

    def read_row(self, row_num=0):
        self.re_reader()
        row = []
        for line in self.reader:
            row.append(line[row_num])
        return row

    def close_file(self):
        self._file.close()


if __name__ == "__main__":
    csv_reader = CsvReader(alarm_file)
    csv_reader.get_by_id_index('10009')
    alarm_dict = csv_reader.build_dict_by_id()
# keys = alarm_dict.keys()
