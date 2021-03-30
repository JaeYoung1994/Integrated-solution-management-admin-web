#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
import pymysql
from common.db.config.dbConfig import DBConfig

#싱글톤 패턴으로 단 한번의 DB 커넥션을 가진다.
class MariaDB:
    _instance = None
    _dbConn = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def connect(cls):
        if not cls._dbConn:
            config = DBConfig()
            dbInfo = config.mariaDB.server_web()
            # DB 연결
            cls._dbConn = pymysql.connect(
                host=dbInfo["host"], # 호스트 정보
                user=dbInfo["user"], # 계정 정보
                password=dbInfo["password"], # 패스워드 정보
                port=dbInfo['port'],
                db=dbInfo["db"], # db 정보
                charset=dbInfo["charset"], # 문자열 정보
                autocommit=True,
                cursorclass=pymysql.cursors.DictCursor
            )
        return cls._dbConn

    def close(cls):
        if cls._dbConn:
            cls._dbConn.close();
