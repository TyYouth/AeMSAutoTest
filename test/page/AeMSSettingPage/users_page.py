#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from test.page.base_page import BasePage
from selenium.webdriver.common.by import By

from utils.time_handler import DateTime


class UsersPage(BasePage):

    def __init__(self, driver):
        super(UsersPage, self).__init__(driver)
        self.column_names = None
        self.default_pwd = "casa1234"
        # attr value of user page
        self.v_add_user_btn = "addUser()"
        self.v_default_pwd_btn = "generateDefault()"
        self.v_account_expiration_select_box = "modal.user.userValidity"
        self.v_pwd_expiration_select_box = "modal.user.passwordValidity"
        self.v_user_pwd_input_text = "modal.user.password"
        self.v_confirm_pwd_input_text = "modal.user.confirmpassword"
        self.v_permission_select_box = "selectedGroups"

        # element of user page
        # self.e_permission_select = (By.XPATH, "//select[@ng-model='selectedGroups']")
        self.e_username = (By.NAME, 'username')
        self.e_given_name = (By.NAME, 'truename')
        self.e_account_expiration = (By.NAME, 'userValidity')
        self.e_pwd_expiration = (By.NAME, 'passwordValidity')
        self.e_confirm_pwd = (By.NAME, 'confirmpassword')
        self.e_primary_phone = (By.NAME, "phone1")
        self.e_secondary_phone = (By.NAME, 'phone2')

    # action of user page
    def action_click_add_btn(self):
        self.button(self.v_add_user_btn)

    def action_fill_user_info(self, username='Admin', user_pwd=None, permission_group='Admin', given_name="autoTest",
                              is_expiration_never=True, account_days_delta=None, pwd_days_delta=None):
        self.action_click_add_btn()
        self.send_keys(self.e_username, username)
        self.send_keys(self.e_given_name, given_name)
        self.select_box(self.v_permission_select_box, text=permission_group)
        # self.select_by_text(self.e_permission_select, permission_group)
        # if the expiration is never
        if is_expiration_never:
            self.select_box(self.v_account_expiration_select_box, value="never")
            self.select_box(self.v_pwd_expiration_select_box, value="never")
        elif (not is_expiration_never) and account_days_delta and pwd_days_delta:
            account_expiration = DateTime.expected_time(days_delta=account_days_delta)
            self.send_keys(self.e_account_expiration, account_expiration)
            password_expiration = DateTime.expected_time(days_delta=pwd_days_delta)
            self.send_keys(self.e_pwd_expiration, password_expiration)
        # fill in default pwd
        if not user_pwd:
            self.button(self.v_default_pwd_btn)
            self.send_keys(self.e_confirm_pwd, self.default_pwd)
        else:
            self.input_text(self.v_user_pwd_input_text, user_pwd)
            self.input_text(self.v_confirm_pwd_input_text, user_pwd)
        # 这个时间控件有毒, 不知道为什么
        # self.click(self.e_pwd_expiration)
        sleep(0.5)
