#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
import logging
import re

class Utils:
    '''
        Parameter description
        dic = Dictionary requiring the presence or absence of a key
        haskKey = List of keys to check
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
    def isEmail(cls, email: str):
        result = bool(re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))
        return result