#!/usr/bin/env python
# coding=utf-8

from time import sleep
from test.common.AeMSCase import AeMSCase
from test.page.basepage import BasePage
from utils.config import Config
from utils.henb import henb

driver = AeMSCase().driver
config_page = BasePage(driver=driver)


class TestModels(AeMSCase, BasePage):
    version = Config().get("AeMS").get("version")
    v_add_btn = "add()"
    v_model_name_input_text = "modelName"
    v_vendor_input_text = "manu"
    v_oui_input_text = "oui"
    v_product_class_input_text = "displays"

    def setUp(self):
        AeMSCase.setUp(self)
        self.open_tab(" Small Cell Management", "Small Cell Models")

    def test_add_model(self):
        henb.get_device_info()
        henb.close()
        self.button(self.v_add_btn)
        self.input_text(self.v_model_name_input_text, self.version + "_HeNB")
        self.find_xpath("input", "value", "input")
        self.click(self.find_xpath("input", "value", "input"))
        self.input_text(self.v_vendor_input_text, henb.device_info['Manufacturer'])
        self.input_text(self.v_oui_input_text, henb.device_info['ManufacturerOUI'])
        self.input_text(self.v_product_class_input_text, henb.device_info['ProductClass'])
        # self.ok_btn()

    def tearDown(self):
        AeMSCase.tearDown(self)
