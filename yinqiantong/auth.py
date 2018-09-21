# -*- coding: utf-8 -*-

import time
import hashlib


class Auth(object):
    def __init__(self, app_id, app_key, app_secret):
        self.__app_id = app_id
        self.__app_key = app_key
        self.__app_secret = app_secret

    def create_sign(self, data=None, ts=None):
        if not ts:
            ts = long(time.time())
        origin_sign_str = ''
        if data:
            keys = sorted(data.keys())
            for k in keys:
                v = data.get(k)
                origin_sign_str += '%s=%s&' % (k, v)
        origin_sign_str += 'ts=%s&app_secret=%s' % (ts, self.__app_secret)
        return hashlib.md5(origin_sign_str).hexdigest()
