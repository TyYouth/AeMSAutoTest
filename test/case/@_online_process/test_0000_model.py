#!/usr/bin/env python
# coding=utf-8
import collections
from time import sleep
from test.common.AeMSCase import AeMSCase
from test.page.SmallCellMgtPage.ModelsPage import ModelsPage
from utils.HeNB import HeNB

driver = AeMSCase().driver
models_page = ModelsPage(driver=driver)


class TestModels(AeMSCase):

    def setUp(self):
        AeMSCase.setUp(self)
        models_page.act_open_tab("Small Cell Management", "Small Cell Models")
        if models_page.column_names is None:
            models_page.column_names = models_page.get_column_names()

    def test_00000_model_is_exited(self):
        """Test is the HeNB or simulator model was is existed or not"""
        device_info = HeNB().get_device_info()
        HeNB().close()
        model_name = self.version + "_HeNB"
        is_existed = models_page.is_model_existed(model_name=model_name, model_info=device_info)
        self.assertTrue(is_existed)
        if is_existed is False:
            models_page.act_add_model(model_name=model_name, model_info=device_info)
            models_page.ok_btn()

    def test_00010_add_model(self):
        """Test model existed prompt"""
        device_info = HeNB().get_device_info()
        HeNB().close()
        model_name = self.version + "_HeNB"
        models_page.act_add_model(model_name, device_info)
        models_page.ok_btn()

    def tearDown(self):
        AeMSCase.tearDown(self)
