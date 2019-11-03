#!/usr/bin/env python
# coding=utf-8
from time import sleep
from test.common.AeMSCase import AeMSCase
from test.page.basepage import BasePage
from test.page.SmallCellManagemetPage import FileManagementPage

driver = AeMSCase().driver
file_management_page = FileManagementPage(driver=driver)


class TestFileManagement(AeMSCase, BasePage):

    def setUp(self):
        AeMSCase.setUp(self)
        # if self._e_cancel_btn:
        #     self.click(self._e_cancel_btn)
        self.open_tab(" Small Cell Management", "File Management")
        if not self._column_names:
            self._column_names = self.get_column_names()

    def test_0001_upload(self):
        pass

    def tearDown(self):
        AeMSCase.tearDown(self)
