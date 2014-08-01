#!/usr/bin/env python
#

import requests


class loremlogsum_http(object):
    key = None
    endpoint = None

    def __init__(self, key, endpoint):
        self.key = key
        self.endpoint = endpoint

    def send(self, line):
        payload = { 'key': self.key, 'log': line }
        requests.get(self.endpoint, params=payload)

