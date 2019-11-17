#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from time import sleep

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

from utils.log import logger
from utils.config import Config
from test.page.LoginPage import LoginPage


class AeMSCase(unittest.TestCase):
    set_up = LoginPage()
    set_up.driver_init()
    driver = set_up.get_driver()
    column_names = None

    @classmethod
    def setUpClass(cls):
        logger.info("start to execute case of " + cls.__module__)
        aems_config = Config().get('AeMS')
        cls.version = aems_config.get('version')
        northbound_ip_address = aems_config.get('northbound_ip_address')
        url = 'https://{0}/hems-web-ui/signin'.format(northbound_ip_address)
        cls.driver.get(url)
        cls.set_up.login_aems()
        cls.timeout = 10
        sleep(0.5)

    def setUp(self):
        logger.info("start test:  " + self._testMethodName)

    def tearDown(self):
        logger.info("test completely:  " + self._testMethodName)

    @classmethod
    def tearDownClass(cls):
        cls.set_up.quit()
        logger.info("complete execute case of " + cls.__module__)

    # https://blog.csdn.net/huilan_same/article/details/52541680
    def open_tab(self, first_tab, second_tab=None, third_tab=None):
        # 注意！ first_tab_name复制前端的字符串（因为可能前端开发为了排版使用空格）
        first_tab_class_name = self.driver.find_element_by_xpath(
            "//a[text()='%s']/parent::li" % first_tab).get_attribute("class")
        if first_tab_class_name == "sub-menu":  # 判断标签是否已经展开
            self.driver.find_element_by_xpath("//a[text()='%s']" % first_tab).click()
        if first_tab_class_name == "sub-menu toggled":
            pass

        if second_tab:
            second_tab_class_name = self.driver.find_element_by_xpath(
                "//a[text()='%s']/parent::li" % second_tab).get_attribute("class")
            if second_tab_class_name:
                if second_tab_class_name == "sub-menu toggled":
                    pass
                # if second_tab_class_name == "sub-menu":
                #     self.driver.find_element_by_xpath("//a[text()='%s']" % second_tab).click()
            else:
                try:
                    self.driver.find_element_by_xpath("//a[text()='%s']" % second_tab).click()
                except ElementNotVisibleException:
                    self.driver.find_element_by_xpath("//a[text()='%s' and @ng-show='true']" % second_tab).click()

        if third_tab:
            third_tab_class_name = self.driver.find_element_by_xpath(
                "//a[text()='%s']/parent::li" % third_tab).get_attribute("class")
            if third_tab_class_name:
                if third_tab_class_name == "sub-menu toggled":
                    pass
            else:
                try:
                    self.driver.find_element_by_xpath("//a[text()='%s']" % second_tab).click()
                except ElementNotVisibleException:
                    self.driver.find_element_by_xpath("//a[text()='%s' and @ng-show='true']" % second_tab).click()
        sleep(0.5)

    # 获取列名
    def get_column_names(self):
        column_names = ()
        try:
            xpath = "//div[@col-index='renderIndex']"
            results = self.driver.find_elements_by_xpath(xpath)
            for column_name in results:
                column_names += (column_name.text,)
            logger.debug("the column names of current web is {}".format(column_names))
        except NoSuchElementException as e:
            logger.exception(e)
        finally:
            return column_names

    # 获取某值的Index
    @staticmethod
    def get_index_of_tuple(original_tuple, value):
        try:
            return original_tuple.index(value)
        except ValueError:
            logger.error(ValueError)
            logger.error("Failed to get {} from tuple {}".format(value, original_tuple))

    # 这里用于寻找列表中的整行内容
    def get_row_by_text(self, label_name, text_val, attr='ng-repeat'):
        try:
            # 根据text寻找其包含ng-repeat属性的div先辈ancestor
            row_text_element = self.driver.find_element_by_xpath(
                "//{}[text()='{}']/ancestor::div[@{}]".format(label_name, text_val, attr))
            row_val = row_text_element.text.split("\n")
            logger.debug("the value of whole row is: {}".format(row_val))
            return row_val
        except NoSuchElementException as e:
            logger.error("Can NOT find the whole row text by {}".format(text_val))
            logger.exception(e.msg)

    # is a text unique on the web, for get its line number
    def is_text_unique(self, label_name, unique_text):
        num_of_text = self.driver.find_elements_by_xpath("//{}[text()='{}']".format(label_name, unique_text))
        if num_of_text == 1:
            return True
        else:
            logger.warning("The {} is NOT unique on the web, the result may not correct".format(unique_text))
            return False

    # 根据唯一值(最好)来获取其属性值value
    def get_val_by_unique_text(self, unique_text, value, label_name='div'):
        attribute_names = self.get_column_names()
        index = self.get_index_of_tuple(attribute_names, value)
        self.is_text_unique(label_name, unique_text)
        row_texts = self.get_row_by_text(label_name, unique_text)
        return row_texts[index]

    # 处理div对话框
    def get_alert_text_and_dismiss(self):
        alert = None
        try:
            sleep(1)
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
