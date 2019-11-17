#!/usr/bin/env python
# coding=utf-8
import os
from time import sleep
from utils.log import logger
from test.common.AeMSCase import AeMSCase
from test.page.SmallCellManagemetPage.FileManagementPage import FileManagementPage

driver = AeMSCase().driver
file_management_page = FileManagementPage(driver=driver)


class TestFileManagement(AeMSCase, FileManagementPage):

    def setUp(self):
        AeMSCase.setUp(self)
        self.open_tab(" Small Cell Management", "File Management")
        if not AeMSCase.column_names:
            AeMSCase.column_names = self.get_column_names()

    def test_0001_upload(self):
        files = self.get_upload_files(self.version)
        # to upload all profile which is format is .csv
        for file in files:
            if file.endswith(".csv"):
                file_management_page.act_upload_file(file)
                sleep(0.25)
                self.find_xpath_by_text('button', 'Confirm').click()
                self.get_alert_text_and_dismiss()
                sleep(0.25)

    def test_0002_test(self):
        print(2)

    def tearDown(self):
        AeMSCase.tearDown(self)
