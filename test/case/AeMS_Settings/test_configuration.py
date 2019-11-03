#!/usr/bin/env python
# coding=utf-8

from time import sleep
from test.common.AeMSCase import AeMSCase
from test.page.basepage import BasePage
from test.page.AeMSSettingPage.ConfigrurationPage import ConfigurationPage

driver = AeMSCase().driver
config_page = ConfigurationPage(driver=driver)


class TestConfigs(AeMSCase, BasePage):

    def setUp(self):
        AeMSCase.setUp(self)
        self.open_tab("AeMS Settings", "Configuration")

    def test_00_sys_setting_prompt(self):
        """test prompt of system setting"""
        # config_page.send_keys(config_page.e_logout_time_input_text, 0)
        # prompt_msg = self.prompt_msg("sysForm.logoutTime.$dirty&&sysForm.logoutTime.$invalid")
        # self.assertEqual("Value should be integer and between 15-60.", prompt_msg)
        # self.assertFalse(
        #     config_page.is_button_enable(config_page.button(config_page.v_sys_save_btn,
        #                                                     is_click=False), "save button"))
        logout_time_show_value = "sysForm.logoutTime.$dirty&&sysForm.logoutTime.$invalid"
        result = config_page.act_input_text_prompt(input_text_ele=config_page.e_logout_time_input_text,
                                                   input_value=0,
                                                   show_value=logout_time_show_value,
                                                   expected_msg="Value should be integer and between 15-60.",
                                                   button_name="save button")
        self.assertTrue(result)

        result = config_page.act_input_text_prompt(input_text_ele=config_page.e_logout_time_input_text,
                                                   input_value=66,
                                                   show_value=logout_time_show_value,
                                                   expected_msg="Value should be integer and between 15-60.",
                                                   button_name="save button")
        self.assertTrue(result)

        result = config_page.act_input_text_prompt(input_text_ele=config_page.e_logout_time_input_text,
                                                   input_value="2@Admin",
                                                   show_value=logout_time_show_value,
                                                   expected_msg="Value should be integer and between 15-60.",
                                                   button_name="save button")
        self.assertTrue(result)

        # config_page.send_keys(config_page.e_logout_time_input_text, 60)
        # self.assertTrue(
        #     config_page.is_button_enable(config_page.button(config_page.v_sys_save_btn, is_click=False)
        #                                  , "save button"))

        result = config_page.act_input_text_prompt(input_text_ele=config_page.e_logout_time_input_text,
                                                   input_value=60,
                                                   button_name="save button", is_false=False)
        self.assertTrue(result)

        result = config_page.act_input_text_prompt(input_text_ele=config_page.e_logout_time_input_text,
                                                   input_value=15,
                                                   button_name="save button", is_false=False)
        self.assertTrue(result)

        result = config_page.act_input_text_prompt(input_text_ele=config_page.e_logout_time_input_text,
                                                   input_value=45,
                                                   button_name="save button", is_false=False)
        self.assertTrue(result)

    def test_01_switch_log_setting(self):
        self.click(self.find_xpath_by_text("button", "Log setting"))
        sleep(0.5)

    def tearDown(self):
        AeMSCase.tearDown(self)
