#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
from common.db.redisDB import RedisDB
from uuid import uuid4

#싱글톤 패턴으로 단 한번의 DB 커넥션을 가진다.
class Session:
    _instance = None
    _dbConn = None
    _prefix = 'was_t0001:session_key:'
    _timeout = 3600

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls._dbConn = RedisDB().connect()
        return cls._instance

    def createSession(cls, username):
        skey = str(uuid4())
        for key in cls._dbConn.keys(cls._prefix+"*"):
            if cls._dbConn.get(key) == username:
                cls.deleteSession(key)
        cls._dbConn.setex(cls._prefix + skey, cls._timeout, username)
        return skey

    def checkSession(cls, skey):
        result = False
        username = cls._dbConn.get(cls._prefix + skey)
        if username is not None:
            cls._dbConn.expire(cls._prefix + skey, cls._timeout)
            result = True
        return result

    def deleteSession(cls, skey):
        cls._dbConn.delete(cls._prefix +skey)