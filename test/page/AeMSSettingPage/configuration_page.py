#!/usr/bin/env python
# coding=utf-8

from test.page.base_page import BasePage
from selenium.webdriver.common.by import By


class ConfigurationPage(BasePage):
    def __init__(self, driver):
        super(ConfigurationPage, self).__init__(driver)
        # attr value of configuration page
        self.v_sys_save_btn = "save()"
        self.v_alarm_save_btn = "saveAlarmStoragePeriod()"
        self.v_name_save_btn = "saveName()"
        self.v_loc_save_btn = "saveGeoInfo()"
        self.v_logout_time_show_value = "sysForm.logoutTime.$dirty&&sysForm.logoutTime.$invalid"

        # element of user page
        self.e_logout_time_input_text = (By.NAME, "logoutTime")
        self.e_pwd_expiration_prompt_input_text = (By.NAME, "pswExpiredDay")
        self.e_pwd_error_lockout_time_input_text = (By.NAME, "pswLockTime")
        self.e_pwd_error_allow_times_input_text = (By.NAME, "pswErrorTime")
        self.e_alarm_time_input_text = (By.NAME, "timeLimit")
        self.e_alarm_size_input_text = (By.NAME, "capacityLimit")
        self.e_aems_name_input_text = (By.NAME, "aemsName")
        self.e_latitude_input_text = (By.NAME, "latitude")
        self.e_longitude_input_text = (By.NAME, "longtitude")
