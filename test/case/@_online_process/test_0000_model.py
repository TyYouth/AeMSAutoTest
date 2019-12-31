#!/usr/bin/env python
# coding=utf-8

from time import sleep
from test.common.AeMSCase import AeMSCase
from test.page.basepage import BasePage
from utils.henb import HeNB

driver = AeMSCase().driver
models_page = BasePage(driver=driver)


class TestModels(AeMSCase):
    v_add_btn = "add()"
    v_model_name_input_text = "modelName"
    v_vendor_input_text = "manu"
    v_oui_input_text = "oui"
    v_product_class_input_text = "displays"

    def setUp(self):
        AeMSCase.setUp(self)
        models_page.act_open_tab("Small Cell Management", "Small Cell Models")
        if models_page.column_names is None:
            models_page.column_names = models_page.get_column_names()

    def test_add_model(self):
        device_info = HeNB().get_device_info()
        HeNB().close()
        models_page.button(self.v_add_btn)
        models_page.input_text(self.v_model_name_input_text, self.version + "_HeNB")
        models_page.find_xpath("input", "value", "input")
        models_page.click(models_page.find_xpath("input", "value", "input"))
        models_page.input_text(self.v_vendor_input_text, device_info['Manufacturer'])
        models_page.input_text(self.v_oui_input_text, device_info['ManufacturerOUI'])
        models_page.input_text(self.v_product_class_input_text, device_info['ProductClass'])
        # self.ok_btn()

    def test_get_model_info(self):
        models_page.get_val_by_unique_text('Simulator', 'OUI')

    def tearDown(self):
        AeMSCase.tearDown(self)
