#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
from common.db.redisDB import RedisDB

#싱글톤 패턴으로 단 한번의 DB 커넥션을 가진다.
class CommandRedis:
    _instance = None
    _dbConn = None
    _prefixCommand = 'worker_command_t0001:ip:'
    _timeout = 7200

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls._dbConn = RedisDB().connect()
        return cls._instance

    def registCommand(cls, ip, token):
        result = True
        for key in cls._dbConn.keys(cls._prefixCommand+"*"):
            if cls._dbConn.get(key) == token:
                cls.deleteSession(key)
        cls._dbConn.setex(cls._prefixCommand + ip, cls._timeout, token)
        return result

    def getRegistCommand(cls):
        keys = cls._dbConn.keys(cls._prefixCommand+"*")
        command = {}
        for key in keys:
            commandKey = key.replace("worker_command_t0001:ip:","")
            command[commandKey] = cls._dbConn.get(key)
        return command

    def checkCommand(cls, ip, token):
        result = False
        username = cls._dbConn.get(cls._prefixCommand + ip)

        if username is not None:
            if username == token:
                cls._dbConn.expire(cls._prefixCommand + ip, cls._timeout)
                result = True
            else:
                result = cls.regist(ip, token)
        return result

    def deleteCommand(cls, ip):
        result = True
        cls._dbConn.delete(cls._prefixCommand + ip)
        return result