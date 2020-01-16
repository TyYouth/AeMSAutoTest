#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from time import sleep
from test.page.base_page import BasePage
from utils.common.log import logger


class ModelsPage(BasePage):

    def __init__(self, driver):
        super(ModelsPage, self).__init__(driver)
        # element of add button
        self.v_add_btn = "add()"
        self.v_model_name_input_text = "modelName"
        self.v_vendor_input_text = "manu"
        self.v_oui_input_text = "oui"
        self.v_product_class_input_text = "displays"
        self.v_ok_btn = "confirm()"
        self.v_cancel_btn = "$close()"

    def is_model_existed(self, model_name, model_info: dict):
        is_exist = False
        whole_list = self.get_whole_list()
        vendor = model_info.get('Vendor')
        oui = model_info.get("OUI")
        product_class = model_info.get("ProductClass")

        for i in range(len(whole_list)):
            if model_name in whole_list[i][0]:
                is_exist = True
                logger.debug("this model name {} was existed".format(model_name))
                break
            if (vendor in whole_list[i]) and (oui in whole_list[i]) and (product_class in whole_list[i]):
                is_exist = True
                logger.warning("this model info {} corresponding model was existed".format(model_info))
        sleep(0.25)
        return is_exist

    def act_add_model(self, model_name, model_info):
        self.button(self.v_add_btn)
        self.checkbox(model_name="status", value="input", to_select=True)
        self.input_text(self.v_model_name_input_text, model_name)
        self.input_text(self.v_vendor_input_text, model_info['Vendor'])
        self.input_text(self.v_oui_input_text, model_info['OUI'])
        self.input_text(self.v_product_class_input_text, model_info['ProductClass'])
        result = True
        return result

    def ok_btn(self):
        ok_btn = self.button(self.v_ok_btn, to_click=False)
        if self.is_button_enable(ok_btn):
            self.click(ok_btn)

    def cancel_btn(self):
        cancel_btn = self.button(self.v_cancel_btn, to_click=False)
        if self.is_button_enable(cancel_btn):
            self.click(cancel_btn)


