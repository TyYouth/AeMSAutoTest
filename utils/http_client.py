#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
from requests import session
from requests import exceptions
from utils.common.log import logger

# basic_url = 'https://api.github.com'


class HTTPClient(object):
    def __init__(self, basic_url, auth=None, headers=None, cookies=None, params=None):
        self._basic_url = basic_url
        self.session = session()
        self.url = None
        if auth:
            self.session.auth = auth
        if headers:
            self.session.headers.update(headers)
        if cookies:
            self.session.cookies.update(cookies)
        if params:
            self.session.params.update(params)

    def build_url(self, endpoint):
        self.url = '/'.join([self._basic_url, endpoint])
        return self.url

    def get(self):
        get_req = self.session.request('GET', self.url)
        logger.debug(get_req.request.headers)
        logger.debug(get_req.request.body)
        logger.debug(get_req.status_code)
        logger.debug(get_req.text)
        return get_req.status_code

    def post(self, data=None, json_data=None):
        post_req = None
        if data:
            post_req = self.session.request('POST', self.url, data=data)
        elif json_data:
            post_req = self.session.request('POST', self.url, json=json_data)
        logger.debug(post_req.request.headers)
        logger.debug(post_req.request.body)
        logger.debug(post_req.status_code)
        return post_req.status_code

    def delete(self, data):
        if data:
            delete_req = self.session.request('DELETE', self.url, data=data)
            logger.debug(delete_req.status_code)

    def close(self):
        self.session.__exit__()

    def __destroy(self):
        self.close()


