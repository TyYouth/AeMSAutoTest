#!/usr/bin/env python
# coding=utf-8

from time import sleep
from utils.common.log import logger
from test.common.aems_case import AeMSCase
from test.page.AeMSSettingPage.configuration_page import ConfigurationPage
from utils.common.utx import Tag, tag

driver = AeMSCase().driver
config_page = ConfigurationPage(driver=driver)


class TestConfigs(AeMSCase):

    def setUp(self):
        AeMSCase.setUp(self)
        config_page.act_open_tab("AeMS Settings", "Configuration")

    @tag(Tag.MEDIUM)
    def test_sys_setting_prompt(self):
        """test prompt of system setting"""
        v_logout_time_show_value = "sysForm.logoutTime.$dirty&&sysForm.logoutTime.$invalid"
        logout_time_input_text = config_page.e_logout_time_input_text
        excepted_logout_time_prompt_msg = "Value should be integer and between 15-60."
        input_values = ["0", "65", "ab@1"]
        for input_value in input_values:
            logger.debug("test for input value: {}".format(input_value))
            prompt_msg = config_page.act_input_text(input_text_ele=logout_time_input_text,
                                                    input_value=input_value,
                                                    is_false=True,
                                                    show_value=v_logout_time_show_value)
            sleep(0.25)
            self.assertEqual(excepted_logout_time_prompt_msg, prompt_msg)

    def tearDown(self):
        AeMSCase.tearDown(self)
