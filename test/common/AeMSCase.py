#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from time import sleep
from utils.log import logger
from utils.config import Config
from test.page.LoginPage import LoginPage


class AeMSCase(unittest.TestCase):
    set_up = LoginPage()
    set_up.driver_init()
    driver = set_up.get_driver()

    @classmethod
    def setUpClass(cls):
        logger.info("start to execute case of " + cls.__module__)
        aems_config = Config().get('AeMS')
        cls.version = aems_config.get('version')
        northbound_ip_address = aems_config.get('northbound_ip_address')
        url = 'https://{0}/hems-web-ui/signin'.format(northbound_ip_address)
        cls.driver.get(url)
        cls.set_up.act_login_aems()
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



