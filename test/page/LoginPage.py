#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from test.page.basepage import BasePage
from selenium.webdriver.common.by import By
from utils.log import logger


class LoginPage(BasePage):
    def __init__(self, driver=None):
        super(LoginPage, self).__init__(driver)
        self.e_username = (By.ID, "username")
        self.e_pwd = (By.ID, "password")
        self.e_repository = (By.NAME, 'repository')
        self.val_login_btn = "login()"

    def act_login_aems(self, login_method='Local Database'):
        self.send_keys(self.e_username, 'admin')
        self.send_keys(self.e_pwd, "casa")
        current_method = self.get_text(self.e_repository)
        logger.debug("current login method is {}".format(current_method))
        self.select_by_text(self.e_repository, login_method)
        self.button(self.val_login_btn)
        sleep(0.5)
