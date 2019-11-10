import os
import datetime
import time
from types import MethodType
from selenium.webdriver.common.by import By
from utils.log import logger
from utils.config import DRIVER_PATH
from test.common.browser import Browser

CHROME_DRIVER_PATH = os.path.join(DRIVER_PATH, 'chromedriver.exe')


class IncorrectPathWebElement(Exception):
    pass


class BasePage(Browser):
    def __init__(self, driver=None):
        # if driver has been init, not need to init again
        if driver:
            self.driver = driver
        else:
            super(BasePage, self).__init__(browser_type='chrome')
        self.by_method = [By.ID, By.NAME, By.CLASS_NAME, By.CSS_SELECTOR, By.XPATH, By.TAG_NAME, By.PARTIAL_LINK_TEXT,
                          By.LINK_TEXT]
        # 遍历对象属性(和方法函数)
        # Traverse object properties (and method functions)
        self._dict = object.__getattribute__(self, '__dict__')
        # general element in all page, start with _e_
        self._e_logout_btn = (By.XPATH, "//li[@ng-click='signOut()']")
        self._e_ok_btn = (By.XPATH, "//button[@ng-click='ok()']")
        self._e_cancel_btn = (By.XPATH, "//button[@ng-click='cancel()']")
        self._e_file_select_input = (By.XPATH, "//input[@ng-file-select='onFileSelect($files)']")
        # self._e_column_name = (By.XPATH, "//div[@col-index='renderIndex']")
        # self._v_add_btn = "add()"

    def __getattribute__(self, attr):
        """
        :param attr: attribute of class object
        :return: web element found by web driver
        """
        # filtering out the attribute which is start with _e_ or _e
        # the _e_ is the generic element of all page
        try:
            if attr.startswith('_e_') or attr.startswith('e_'):
                value = self._dict[attr]
                if isinstance(value, tuple) and len(value) == 2 and value[0] in self.by_method:
                    _web_element = self.find_element(*value)
                    return _web_element
                else:
                    raise IncorrectPathWebElement('{} is incorrect web element'.format(str(value)))
            else:
                return object.__getattribute__(self, attr)
        except AttributeError as e:
            logger.exception(e)

    @staticmethod
    def expected_time(days_delta=0, min_delta=0):
        """
            :param days_delta: int, delta day
            :param min_delta: int, delta minute
            :return: expected time
        """
        expected_time = datetime.datetime.now() + datetime.timedelta(days=days_delta, minutes=min_delta)
        return expected_time.strftime('%Y-%m-%d %H:%M:%S')

    # Most of the aems input text include similar content: <input type="text ng-model="modal.data.alarmId">
    def input_text(self, model_value, keys=None, clear_first=True):
        """
        :param model_value: value of ng-model
        :param keys: keys to input
        :param clear_first: clear input text first or not
        :return: if kes is not return element location
        """
        elem_loc = self.find_xpath("input", "ng-model", model_value)
        if keys:
            self.send_keys(elem_loc, keys, clear_first)
        else:
            return elem_loc

    # Most of the drop-down boxes include similar content <select  ng-model="modal.user.userValidity" </select>
    def select_box(self, model_value, index=None, value=None, text=None):
        select_ele = self.find_xpath("select", "ng-model", model_value)
        if index:
            self.select_by_text(select_ele, index)
        elif value:
            self.select_by_value(select_ele, value)
        elif text:
            self.select_by_text(select_ele, text)
        else:
            return select_ele

    # Most of the BUTTONS include similar content <button class="class value" ng-click="login()">Login</button>
    def button(self, click_value, is_click=True):
        """
        find button by value and click
        :param click_value:  value of ng-click
        :param is_click: click or not
        :return: None
        """
        button_element = self.find_xpath("button", "ng-click", click_value)
        if is_click:
            self.click(button_element)
        else:
            return button_element

    def is_button_enable(self, web_ele):
        is_disabled = self.get_attr(web_ele, "disabled")
        # the value return by get_attr is true or false
        if is_disabled == 'true':
            logger.error("This OK button can NOT be clicked")
            return False
        # wrong maybe
        else:
            logger.debug("This button may be clicked")
            return True

    def is_ok_btn_enable(self):
        self.is_button_enable(self._e_ok_btn)

    def ok_btn(self):
        if self.is_ok_btn_enable():
            self.click(self._e_ok_btn)
            logger.debug("click the ok button")
            time.sleep(0.25)
        else:
            logger.debug("the ok button is not clickable")

    def cancel_btn(self):
        self.click(self._e_cancel_btn)
        logger.debug("click the cancel button")
        time.sleep(0.25)

    # Most of the prompts include similar content
    # <small class="help-block" ng-show="show value" >msg text</small>
    def prompt_msg(self, show_value=None):
        if show_value:
            prompt_ele = self.find_xpath("small", "ng-show", show_value)
        # if show can not available and class is unique
        # class name will be include "ng-hide" when it's invisible or does not show on web
        else:
            prompt_ele = self.find_class("help-block")
        msg = self.get_text(prompt_ele)
        logger.debug("the prompt msg is: {}".format(msg))
        return msg

    # Action for base page
    def act_logout_aems(self):
        self.click(self._e_logout_btn)
        self.ok_btn()

    def act_input_text_prompt(self, input_text_ele, input_value, show_value=None, expected_msg=None,
                              is_false=True):
        self.send_keys(input_text_ele, input_value)
        result = False
        if is_false:
            prompt_msg = self.prompt_msg(show_value=show_value)
            if expected_msg == prompt_msg and (self.is_button_enable(self.button(self.v_sys_save_btn, is_click=False)
                                                                     ) is False):
                result = True
        elif not (is_false and show_value and expected_msg):
            if self.is_button_enable(self.button(self.v_sys_save_btn, is_click=False)) is True:
                result = True
        return result

    def act_upload_file(self, file_path):
        self.button('upload()')
        self.upload_file(self._e_file_select_input, file_path)
        try:
            # it is a ok button in fact
            self.ok_btn()
        except:
            self.find_xpath_by_text('button', 'Upload')
