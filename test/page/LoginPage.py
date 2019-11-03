#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from test.page.basepage import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    def __init__(self, driver=None):
        super(LoginPage, self).__init__(driver)
        self.e_username = (By.ID, "user_name")
        self.e_pwd = (By.ID, "password")
        self.e_repository = (By.NAME, 'repository')
        self.val_login_btn = "login()"

    def login_aems(self):
        self.send_keys(self.e_username, 'admin')
        self.send_keys(self.e_pwd, "casa")
        self.select_by_text(self.e_repository, 'Local Database')
        self.button(self.val_login_btn)
        sleep(0.5)
