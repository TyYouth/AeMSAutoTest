#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
from test.page.basepage import BasePage
from selenium.webdriver.common.by import By


class FileManagementPage(BasePage):

    def __init__(self, driver):
        super(FileManagementPage, self).__init__(driver)


