#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from test.page.base_page import BasePage
from utils.config import DATA_PATH
from utils.common.log import logger


class FileManagementPage(BasePage):

    def __init__(self, driver):
        super(FileManagementPage, self).__init__(driver)

    @classmethod
    def get_upload_files(cls, version):
        cls.path_list = []
        version_upload_file = os.path.join(DATA_PATH, ''.join([version, '_upload']))
        version_file_paths = os.listdir(version_upload_file)
        if version == 'pico':
            for files_path in version_file_paths:
                if '4.5' in files_path:
                    file_path = "\\".join([version_upload_file, files_path])
                    logger.debug("get version file from: {}".format(file_path))
                    for file in os.listdir(file_path):
                        cls.path_list.append("\\".join([file_path, file]))
        if version == 'femto':
            pass
        return cls.path_list
