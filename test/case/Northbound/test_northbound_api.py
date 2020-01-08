#!/usr/bin/env python
# coding=utf-8

import requests

from utils.Config import Config
from test.page.BasePage import BasePage
from test.common.AeMSCase import AeMSCase

host = Config().get("AeMS").get("northbound_ip_address")
northbound_user_config = Config().get("AeMS").get("northbound_user")
basic_url = "https://{}/hems-web-ui/nbi".format(host)
nodes = {"list": 'nodes/list', "info": 'nodes/info', "alarms": 'nodes/alarms'}


def build_url(endpoint):
    url = '/'.join([basic_url, endpoint])
    return url


driver = AeMSCase().driver
base_page = BasePage(driver=driver)


class TestNorthboundAPI(AeMSCase):

    def setUp(self):
        AeMSCase.setUp(self)
        # base_page.act_open_tab("Small Cell Management")

    def test_00000_create_webservice_user(self):
        """1.to  adjust Webservice is exit or not"""
        pass

    def test_00100_nodes_list(self):
        """Test api: /hems-web-ui/nbi/nodes/list"""
        list_url = build_url(nodes["alarms"])
        headers = {"Accept": 'application/json'}
        req = requests.get(list_url, auth=("ntapi", "casa1234"), verify=False, headers=headers)
        print(req.url)
        print(req.status_code)
        print(req.json())
        print(list_url)

    def tearDown(self):
        AeMSCase.tearDown(self)
