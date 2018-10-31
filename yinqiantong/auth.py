# -*- coding: utf-8 -*-
import time
import json
import urllib2
import hashlib


def http_post_json(url, data=None, headers=None):
    if headers is None:
        headers = {}
    if data is None:
        data = {}
    try:
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        for k, v in headers.items():
            req.add_header(k, v)
        response = urllib2.urlopen(req, json.dumps(data))
        return response.code, response.read()
    except urllib2.HTTPError, e:
        return e.code, e
    except urllib2.URLError, e:
        return 0, e
    except Exception as e:
        return 0, e


def http_get(url, headers=None):
    if headers is None:
        headers = {}
    try:
        req = urllib2.Request(url)
        for k, v in headers.items():
            req.add_header(k, v)
        response = urllib2.urlopen(req)
        return response.code, response.read()
    except urllib2.HTTPError, e:
        return e.code, e
    except urllib2.URLError, e:
        return 0, e
    except Exception as e:
        return 0, e


class Auth(object):
    def __init__(self, app_id, app_secret):
        self.__app_id = app_id
        self.__app_secret = app_secret

    def create_sign(self, data=None):
        if data is None:
            data = {}
        if not data.get('ts'):
            data['ts'] = long(time.time())
        if not data.get('appid'):
            data['appid'] = self.__app_id
        origin_sign_str = ''
        keys = sorted(data.keys())
        for k in keys:
            v = data.get(k)
            if not v or v == '' or k == 'sign' or k == '':
                continue
            origin_sign_str += '%s=%s&' % (k, v)
        origin_sign_str += 'app_secret=%s' % (self.__app_secret)
        return hashlib.md5(origin_sign_str).hexdigest()

    def check_sign(self, data):
        if not data or not data.get('sign'):
            return False
        curr_sign = self.create_sign(data)
        return curr_sign == data.get('sign')

    def create_order(self, data):
        if data is None:
            data = {}
        if not data.get('ts'):
            data['ts'] = long(time.time())
        if not data.get('appid'):
            data['appid'] = self.__app_id
        sign = self.create_sign(data)
        data['sign'] = sign
        (code, data_str) = http_post_json('https://yqtapi.com/order', data)
        res_data = json.loads(data_str)
        if res_data and res_data['data'] and res_data['code'] == 200:
            data['pay_body'] = res_data['data']['pay_body']
            data['out_trade_no'] = res_data['data']['out_trade_no']
            data['expire_time'] = res_data['data']['expire_time']
            res_data['data'] = data
        return res_data

    def get_order_state_by_out_trade_no(self, out_trade_no):
        (code, data_str) = http_get('https://yqtapi.com/order?appid=%s&out_trade_no=%s' % (self.__app_id, out_trade_no))
        res_data = json.loads(data_str)
        return res_data

    def get_order_state_by_client_out_trade_no(self, client_out_trade_no):
        (code, data_str) = http_get(
            'https://yqtapi.com/order?appid=%s&client_out_trade_no=%s' % (self.__app_id, client_out_trade_no))
        res_data = json.loads(data_str)
        return res_data
