#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
import json
from common.db.redisDB import RedisDB

#싱글톤 패턴으로 단 한번의 DB 커넥션을 가진다.
class ClientRedis:
    _instance = None
    _dbConn = None
    _prefixClient = 'worker_client_t0001:ip:'
    _prefixClientDeviceInfo = 'worker_client_t0001:device:'
    _timeout = 7200

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls._dbConn = RedisDB().connect()
        return cls._instance

    def registClient(cls, commandIp, clientIp):
        result = True
        for key in cls._dbConn.keys(cls._prefixClient+"*"):
            if cls._dbConn.get(key) == clientIp:
                result = False
                break;
        cls._dbConn.set(cls._prefixClient + clientIp, commandIp)
        return result

    def getClient(cls):
        keys = cls._dbConn.keys(cls._prefixClient+"*")
        client = {}
        for key in keys:
            clientKey = key.replace(cls._prefixClient, "")
            client[clientKey] = cls._dbConn.get(key)
        return client

    def deleteClient(cls, clientIp):
        result = True
        cls._dbConn.delete(cls._prefixClient + clientIp)
        cls._dbConn.delete(cls._prefixClientDeviceInfo + clientIp)
        return result

    def registClientDevice(cls, clientIp, device):
        result = True
        clientKeys = cls._dbConn.keys(cls._prefixClient + "*")
        clientKey = cls._prefixClient+clientIp
        if clientKey in clientKeys:
            keys = cls._dbConn.keys(cls._prefixClientDeviceInfo + "*")
            key = cls._prefixClientDeviceInfo+clientIp
            if key in keys:
                cls._dbConn.delete(key)
            cls._dbConn.set(key, json.dumps(device, ensure_ascii=False))
        return result

    def deleteClientDevice(cls, clientIp):
        result = True
        cls._dbConn.delete(cls._prefixClient + clientIp)
        cls._dbConn.delete(cls._prefixClientDeviceInfo + clientIp)
        return result

    def getClientDevice(cls):
        clientKeys = cls._dbConn.keys(cls._prefixClient + "*")
        clientDeviceKeys = cls._dbConn.keys(cls._prefixClientDeviceInfo + "*")
        for clientDeviceKey in clientDeviceKeys:
            clientIp = clientDeviceKey.replace(cls._prefixClientDeviceInfo, "")
            clientkey = cls._prefixClient + clientIp
            if clientkey not in clientKeys:
                cls.deleteClientDevice(clientIp)
        clientDeviceKeys = cls._dbConn.keys(cls._prefixClientDeviceInfo + "*")
        clientDevice = {}
        for key in clientDeviceKeys:
            clientDeviceKey = key.replace(cls._prefixClientDeviceInfo, "")
            clientDevice[clientDeviceKey] = json.loads(cls._dbConn.get(key))
        return clientDevice
