#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from test.common.AeMSCase import AeMSCase
from test.page.basepage import BasePage
from test.page.AeMSSettingPage.UsersPage import UsersPage

driver = AeMSCase().driver
users_page = UsersPage(driver=driver)


class TestUsers(AeMSCase, UsersPage):

    def setUp(self):
        AeMSCase.setUp(self)
        if users_page._e_cancel_btn:
            self.click(users_page._e_cancel_btn)
        self.open_tab("AeMS Settings", "Users")

    def test_00_user_tip(self):
        """test the tip of add user"""
        users_page.action_fill_user_info()
        users_page.ok_btn()
        prompt_msg = self.prompt_msg(show_value="isExisted")
        self.assertEqual("The name has already been existed", prompt_msg)

        users_page.send_keys(users_page.e_username, "ab")
        prompt_msg = self.prompt_msg(show_value="setForm.user_name.$dirty && setForm.user_name.$invalid")
        self.assertEqual('required letters number or "_"(3 to 16 characters)', prompt_msg)

        users_page.send_keys(users_page.e_username, "abcdefg0123456789")
        prompt_msg = self.prompt_msg(show_value="setForm.user_name.$dirty && setForm.user_name.$invalid")
        self.assertEqual('required letters number or "_"(3 to 16 characters)', prompt_msg)
        sleep(0.25)

    def test_01_pwd_tip(self):
        """Test the tip of password"""
        users_page.action_fill_user_info(user_name="pwdTip")
        users_page.input_text(users_page.v_user_pwd_input_text, "aaaabbbb")
        prompt_msg = self.prompt_msg(show_value="isNoPassVaild")
        self.assertEqual('At least two kinds of the combination of Uppercase letters, '
                         'Lowercase letters, Numbers, or Special characters(space key is not allow), '
                         'and the length between 8 and 20 characters.', prompt_msg)

        users_page.input_text(users_page.v_user_pwd_input_text, "pwdTiptest")
        users_page.input_text(users_page.v_confirm_pwd_input_text, "pwdTiptest")
        users_page.ok_btn()
        sleep(0.25)
        prompt_msg = self.prompt_msg(show_value="isContainPassword")
        self.assertEqual('Password cannot contain user name !', prompt_msg)

        users_page.input_text(users_page.v_user_pwd_input_text, "Admin1111")
        users_page.input_text(users_page.v_confirm_pwd_input_text, "admin0101")
        prompt_msg = self.prompt_msg(
            show_value="modal.user.password && !isNoPassVaild && setForm.confirmpassword.$invalid")
        self.assertEqual('Passwords do not match', prompt_msg)

    def test_02_phone_tip(self):
        users_page.action_fill_user_info(user_name='phoneTest')
        users_page.ok_btn()
        users_page.send_keys(users_page.e_primary_phone, "(444)-555-666")
        users_page.send_keys(users_page.e_secondary_phone, '(444)-555-666')
        sleep(0.25)
        prompt_msg_1 = self.prompt_msg(show_value='setForm.phone1.$dirty && setForm.phone1.$invalid')
        self.assertEqual('Incorrect phone number format', prompt_msg_1)
        prompt_msg_2 = self.prompt_msg(show_value="setForm.phone2.$dirty && setForm.phone2.$invalid")
        self.assertEqual('Incorrect phone number format', prompt_msg_2)

        users_page.send_keys(users_page.e_primary_phone, "555")
        users_page.send_keys(users_page.e_secondary_phone, '555')
        sleep(0.25)
        prompt_msg_1 = self.prompt_msg(show_value='setForm.phone1.$dirty && setForm.phone1.$invalid')
        self.assertEqual('Incorrect phone number format', prompt_msg_1)
        prompt_msg_2 = self.prompt_msg(show_value="setForm.phone2.$dirty && setForm.phone2.$invalid")
        self.assertEqual('Incorrect phone number format', prompt_msg_2)

        users_page.send_keys(users_page.e_primary_phone, "(444)-555-6666")
        users_page.send_keys(users_page.e_secondary_phone, "(444)-555-6666")
        users_page.ok_btn()
        sleep(0.25)
        prompt_msg = self.prompt_msg("isSame1")
        self.assertEqual('Phone2 should not be the same as Phone1', prompt_msg)

    def tearDown(self):
        AeMSCase.tearDown(self)
