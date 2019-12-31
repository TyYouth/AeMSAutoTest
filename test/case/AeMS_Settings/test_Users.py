#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from utils.common.log import logger
from test.common.AeMSCase import AeMSCase
from test.page.AeMSSettingPage.UsersPage import UsersPage

driver = AeMSCase().driver
users_page = UsersPage(driver=driver)


class TestUsers(AeMSCase):

    def setUp(self):
        AeMSCase.setUp(self)
        users_page.act_open_tab("AeMS Settings", "Users")

    def test_00100_user_prompt(self):
        """test the tip of add user"""
        users_page.action_fill_user_info(username='Admin')
        users_page.ok_btn()
        prompt_msg = users_page.prompt_msg(show_value="isExisted")
        self.assertEqual("The name has already been existed", prompt_msg)

        input_values = ["ab", "abcdefg0123456789", "sdffa@ssq.c"]
        username_input_text = users_page.e_username
        except_wrong_username_prompt = 'required letters number or "_"(3 to 16 characters)'
        v_prompt_msg_show_value = None
        if self.version == "pico":
            v_prompt_msg_show_value = "setForm.user_name.$dirty && setForm.user_name.$invalid"
        elif self.version == "femto":
            v_prompt_msg_show_value = "setForm.username.$dirty && setForm.username.$invalid"
        for input_value in input_values:
            prompt_msg = None
            logger.debug("to test input value: {}".format(input_value))
            prompt_msg = users_page.act_input_text(input_text_ele=username_input_text,
                                                   input_value=input_value,
                                                   is_false=True,
                                                   show_value=v_prompt_msg_show_value)
            sleep(0.25)
            self.assertEqual(except_wrong_username_prompt, prompt_msg)
        users_page.cancel_btn()

    def test_00110_pwd_prompt(self):
        """Test the tip of password"""
        users_page.action_fill_user_info(username="pwdTip")
        users_page.input_text(users_page.v_user_pwd_input_text, "aaaabbbb")
        prompt_msg = users_page.prompt_msg(show_value="isNoPassVaild")
        self.assertEqual('At least two kinds of the combination of Uppercase letters, '
                         'Lowercase letters, Numbers, or Special characters(space key is not allow), '
                         'and the length between 8 and 20 characters.', prompt_msg)

        users_page.input_text(users_page.v_user_pwd_input_text, "pwdTiptest")
        users_page.input_text(users_page.v_confirm_pwd_input_text, "pwdTiptest")
        users_page.ok_btn()
        sleep(0.25)
        prompt_msg = users_page.prompt_msg(show_value="isContainPassword")
        self.assertEqual('Password cannot contain user name !', prompt_msg)

        users_page.input_text(users_page.v_user_pwd_input_text, "Admin1111")
        users_page.input_text(users_page.v_confirm_pwd_input_text, "admin0101")
        prompt_msg = users_page.prompt_msg(
            show_value="modal.user.password && !isNoPassVaild && setForm.confirmpassword.$invalid")
        self.assertEqual('Passwords do not match', prompt_msg)
        users_page.cancel_btn()

    def test_00120_phone_prompt(self):
        """Test phone prompt"""
        users_page.action_fill_user_info(username='phoneTest')
        users_page.send_keys(users_page.e_primary_phone, "(444)-555-666")
        users_page.send_keys(users_page.e_secondary_phone, '(444)-555-666')
        sleep(0.25)

        prompt_msg_1 = users_page.prompt_msg(show_value='setForm.phone1.$dirty && setForm.phone1.$invalid')
        self.assertEqual('Incorrect phone number format', prompt_msg_1)
        prompt_msg_2 = users_page.prompt_msg(show_value="setForm.phone2.$dirty && setForm.phone2.$invalid")
        self.assertEqual('Incorrect phone number format', prompt_msg_2)

        users_page.send_keys(users_page.e_primary_phone, "555")
        users_page.send_keys(users_page.e_secondary_phone, '555')
        sleep(0.25)
        prompt_msg_1 = users_page.prompt_msg(show_value='setForm.phone1.$dirty && setForm.phone1.$invalid')
        self.assertEqual('Incorrect phone number format', prompt_msg_1)
        prompt_msg_2 = users_page.prompt_msg(show_value="setForm.phone2.$dirty && setForm.phone2.$invalid")
        self.assertEqual('Incorrect phone number format', prompt_msg_2)

        users_page.send_keys(users_page.e_primary_phone, "(444)-555-6666")
        users_page.send_keys(users_page.e_secondary_phone, "(444)-555-6666")
        users_page.ok_btn()
        sleep(0.25)
        prompt_msg = users_page.prompt_msg("isSame1")
        self.assertEqual('Phone2 should not be the same as Phone1', prompt_msg)
        sleep(0.25)
        users_page.cancel_btn()

    def tearDown(self):
        AeMSCase.tearDown(self)
