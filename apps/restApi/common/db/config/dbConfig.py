#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
class DBConfig:
    class MariaDB:
        def server_web(self):
            config = {
                "user": "root",
                "password":"2310",
                "host": "127.0.0.1",
                "port": 10001,
                "db": "troll_worker_web",
                "charset": "utf8"
            }
            return config

    class RedisDB:
        def server_web(self):
            config = {
                "password":"2310",
                "host": "127.0.0.1",
                "port": "9001",
                "decode_responses": True
            }
            return config

    def __init__(self):
        self.mariaDB = self.MariaDB()
        self.redisDB = self.RedisDB()
