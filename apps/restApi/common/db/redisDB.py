#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
import redis
from common.db.config.dbConfig import DBConfig

#싱글톤 패턴으로 단 한번의 DB 커넥션을 가진다.
class RedisDB:
    _instance = None
    _dbConn = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def connect(cls):
        if not cls._dbConn:
            config = DBConfig()
            dbInfo = config.redisDB.server_web()

            # DB 연결
            cls._dbConn = redis.Redis(
                host=dbInfo["host"],
                port=dbInfo["port"],
                password=dbInfo["password"],
                decode_responses=dbInfo["decode_responses"]
            )
        return cls._dbConn

    def close(cls):
        if cls._dbConn:
            cls._dbConn.close();
