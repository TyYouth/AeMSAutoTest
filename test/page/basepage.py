import os
import datetime
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from utils.log import logger
from utils.config import DRIVER_PATH
from test.common.browser import Browser
CHROME_DRIVER_PATH = os.path.join(DRIVER_PATH, 'chromedriver.exe')

BY_METHOD = [By.ID, By.NAME, By.CLASS_NAME, By.CSS_SELECTOR, By.XPATH, By.TAG_NAME, By.PARTIAL_LINK_TEXT,
             By.LINK_TEXT]


class IncorrectPathWebElement(Exception):
    pass


class BasePage(Browser):
    column_names = None

    def __init__(self, driver=None):
        # if driver has been init, not need to init again
        if driver:
            self.driver = driver
        else:
            super(BasePage, self).__init__(browser_type='chrome')
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
        # try:
        if attr.startswith('_e_') or attr.startswith('e_'):
            value = self._dict[attr]
            if isinstance(value, tuple) and len(value) == 2 and value[0] in BY_METHOD:
                _web_element = self.driver.find_element(*value)
                return _web_element
            else:
                raise IncorrectPathWebElement('{} is incorrect web element'.format(str(value)))
        else:
            return object.__getattribute__(self, attr)
        # except AttributeError as e:
        #     logger.exception(e)

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
        return self.is_button_enable(self._e_ok_btn)

    def ok_btn(self):
        if self.is_ok_btn_enable():
            self.click(self._e_ok_btn)
            logger.debug("click the ok button")
        else:
            logger.debug("the ok button is not clickable")

    def cancel_btn(self):
        self.click(self._e_cancel_btn)
        logger.debug("click the cancel button")
        time.sleep(0.25)

    def prompt_msg(self, show_value=None):
        """
        # Most of the prompts include similar content
        # <small class="help-block" ng-show="show value" >msg text</small>
        :param show_value: value of ng-show
        :return: str, prompt message
        """
        if show_value is not None:
            prompt_ele = self.find_xpath("small", "ng-show", show_value)
        # if show can not available and class is unique
        # class name will be include "ng-hide" when it's invisible or does not show on web
        else:
            prompt_ele = self.find_class("help-block")
        prompt_msg = self.get_text(prompt_ele)
        logger.debug("the prompt msg is: {}".format(prompt_msg))
        return prompt_msg

    # 处理网管弹出的div警告类对话框
    def get_alert_text_and_dismiss(self):
        alert = None
        try:
            time.sleep(0.5)
            alert = self.driver.find_element_by_xpath("//div[@class='sweet-alert showSweetAlert visible']")
        except NoSuchElementException:
            logger.warning("There is no alert displayed")
        finally:
            if alert:
                text = alert.find_element_by_xpath("//p[@class='lead text-muted']").text
                logger.warning("The alert is shown, and its text is: " + text)
                self.driver.find_element_by_xpath('//button[text()="OK"]').click()
                return text
            else:
                return None

    def get_column_names(self):
        """
        the most column name of AeMS web is like: <div ..... col-index="renderIndex"><span ... >Model</span> </div>
        :return: tuple, column names of list
        """
        column_names = ()
        xpath = "//div[@col-index='renderIndex']"
        results = self.finds_xpath(value=xpath)
        for column_name in results:
            column_names += (column_name.text,)
        logger.debug("the column names of current web is {}".format(column_names))
        return column_names

    def get_row_by_text(self, label_name, text_val, attr='ng-repeat'):
        """
        the most row value of AeMS web is like:
        :param text_val:
        :param label_name:
        :param attr:
        :return:
        """
        # 根据text_val寻找其包含ng-repeat属性的div先辈ancestor
        # Find the ancestor of the div containing which contains `ng-repeat` attribute based on the text_val
        row_text_element = self.find_xpath(
            value="//{}[text()='{}']/ancestor::div[@{}]".format(label_name, text_val, attr))
        row_val = row_text_element.text.split("\n")
        logger.debug("the value of whole row is: {}".format(row_val))
        return row_val

    # 获取某值的Index
    @staticmethod
    def get_index_of_tuple(original_tuple, value):
        """
        to get index of tuple value
        :param original_tuple:
        :param value:
        :return:
        """
        try:
            return original_tuple.index(value)
        except ValueError:
            logger.error(ValueError)
            logger.error("Failed to get {} from tuple {}".format(value, original_tuple))

    def is_text_unique(self, unique_text, label_name):
        """
        get web elems numbers to judge is a text unique on the web,
        :param unique_text:
        :param label_name:
        :return: bool,
        """
        num_of_text = self.finds_xpath(value="//{}[text()='{}']".format(label_name, unique_text))
        if num_of_text == 1:
            return True
        else:
            logger.warning("The {} is NOT unique on the web, the result may not correct".format(unique_text))
            return False

    def get_val_by_unique_text(self, unique_text, attr, label_name='div'):
        """
        Get attr based on unique value (best)
        such as ne_online_status = get_val_by_unique_text(identity, "Node Backhaul Status")
        :param unique_text: str, unique text on the web
        :param attr: str, attr name
        :param label_name:
        :return: attr value
        """
        attribute_names = self.get_column_names()
        index = self.get_index_of_tuple(attribute_names, attr)
        self.is_text_unique(label_name, unique_text)
        row_texts = self.get_row_by_text(label_name, unique_text)
        logger.debug("the attr {} of {} is {}".format(attr, unique_text, row_texts[index]))
        return row_texts[index]

    # Action for base page
    def act_logout_aems(self):
        """Logout AeMS"""
        self.click(self._e_logout_btn)
        self.ok_btn()

    def act_open_tab(self, *tabs_names):
        """
        :param tabs_names: tuple, tabs names
        """
        # 直接使用contains 来忽略为了排版而使用的前端空格, 参数直接为tab name 即可
        tab_parent_xpath = "//a[contains(text(), '{}')]/parent::li"
        for tab in tabs_names:
            # 是否有展开标记的class 属性, 没有的话代表是末尾标签, 直接点击, 不会
            tab_parent_elem = self.find_xpath(value=tab_parent_xpath.format(tab))
            tab_parent_class_attr = self.get_attr(tab_parent_elem, "class")
            if tab_parent_class_attr:
                # if the tab has been not unfolded
                if tab_parent_class_attr == "sub-menu":
                    try:
                        self.click(self.find_xpath_by_text('a', tab))
                    except ElementNotVisibleException:
                        visible_tab_xpath = "//a[contains(text(), '{}') and @data-ui-sref='system.Setting']".format(tab)
                        self.click(self.find_xpath(value=visible_tab_xpath))
                elif tab_parent_class_attr == "sub-menu toggled":
                    pass
            else:
                try:
                    self.click(self.find_xpath_by_text('a', tab))
                except ElementNotVisibleException:
                    visible_tab_xpath = "//a[contains(text(), '{}') and @ng-show='true']".format(tab)
                    self.click(self.find_xpath(visible_tab_xpath))
        time.sleep(0.25)

    def act_input_text(self, input_text_ele, input_value, is_false=True, show_value=None):
        """
        :param input_text_ele: web element of input text
        :param input_value: value to input
        :param is_false: True for negative test
        :param show_value: value of ng-show
        :return: str, prompt message
        """
        self.send_keys(input_text_ele, input_value)
        if is_false and (show_value is not None):
            prompt_msg = self.prompt_msg(show_value)
            return prompt_msg

    def act_upload_file(self, file_path):
        """
        :param file_path: path of file to upload
        """
        self.button('upload()')
        self.upload_file(self._e_file_select_input, file_path)
        try:
            logger.debug("To upload file: " + file_path)
            self.ok_btn()
        except:
            self.find_xpath_by_text('button', 'Upload')
        finally:
            time.sleep(0.5)
