#!/usr/bin/env python
# coding=utf-8
from time import sleep
from test.common.aems_case import AeMSCase
from test.page.SmallCellMgtPage.file_mgt_page import FileManagementPage
from utils.common.utx import Tag, tag

driver = AeMSCase().driver
file_management_page = FileManagementPage(driver=driver)


class TestFileManagement(AeMSCase):

    def setUp(self):
        AeMSCase.setUp(self)
        file_management_page.act_open_tab("Small Cell Management", "File Management")
        if not AeMSCase.column_names:
            AeMSCase.column_names = file_management_page.get_column_names()

    @tag(Tag.HIGH)
    def test_0001_upload(self):
        files = file_management_page.get_upload_files(self.version)
        # to upload all profile which format is .csv (end with csv)
        for file in files:
            if file.endswith(".csv"):
                file_management_page.act_upload_file(file)
                sleep(0.25)
                file_management_page.find_xpath_by_text('button', 'Confirm').click()
                file_management_page.get_alert_text_and_dismiss()
                sleep(0.25)

    def test_0002_test(self):
        print(2)

    def tearDown(self):
        AeMSCase.tearDown(self)
