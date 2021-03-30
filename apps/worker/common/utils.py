#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
import logging
import json
import socket
import requests
from common.init import Init

class Utils:
    '''

    '''
    @classmethod
    def isDicHasKey(cls, dic:dict, haskey:list):
        result = False
        if type(dic) is not dict:
            logging.error("It is not a dictionary.")
            return result

        if type(haskey) is not list:
            logging.error("It is not a list.")
            return result

        result = True
        for key in haskey:
            if key not in dic:
                result = False
                break
        return result

    @classmethod
    def isDicKeyValueNull(cls, dic: dict, chkkey: list):
        result = False
        if type(dic) is not dict:
            logging.error("It is not a dictionary.")
            return result

        if type(chkkey) is not list:
            logging.error("It is not a list.")
            return result

        if cls.isDicHasKey(dic, chkkey):
            result = True
            for key in chkkey:
                if not dic[key]:
                    result = False
                    break
        return result

    @classmethod
    def requestUrl(cls, method=str, url=str, data=None, json=None, params=None, **kwargs):
        method = method.upper()
        if method == "POST":
            res = requests.post(url=url, data=data, json=json, **kwargs)
        elif method == "GET":
            res = requests.get(url=url, params=params)
        return res

    @classmethod
    def ipCheck(cls):
        url = Init.getInitPath() + '/worker/client/authKey'
        res = Utils.requestUrl(method="GET", url=url)
        initJson = json.loads(res.text)
        localIp = socket.gethostbyname(socket.gethostname())
        ip = initJson['ip'] + ":" + localIp
        return ip