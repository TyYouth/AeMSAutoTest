#!/usr/bin/env python
# coding=utf-8
import os
from time import sleep
from utils.log import logger
from utils.config import DATA_FILE
from test.common.AeMSCase import AeMSCase
from test.page.SmallCellManagemetPage.FileManagementPage import FileManagementPage

driver = AeMSCase().driver
file_management_page = FileManagementPage(driver=driver)


class TestFileManagement(AeMSCase, FileManagementPage):

    def setUp(self):
        AeMSCase.setUp(self)
        # if self._e_cancel_btn:
        #     self.click(self._e_cancel_btn)
        self.open_tab(" Small Cell Management", "File Management")
        if not self.version_upload_file:
            self.version_upload_file = os.path.join(DATA_FILE, self.version.join('_upload'))
        if not AeMSCase.column_names:
            AeMSCase.column_names = self.get_column_names()

    def test_0001_upload(self):
        pass

    def test_0002_test(self):
        print(2)

    def tearDown(self):
        AeMSCase.tearDown(self)
