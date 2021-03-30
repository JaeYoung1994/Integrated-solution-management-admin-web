#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
from flask_bcrypt import Bcrypt


class Encryption:
    _instance = None
    _bcrypt = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def setBcrypt(cls, app):
        cls._bcrypt = Bcrypt(app)

    def changeBcrypt(cls, password):
        return cls._bcrypt.generate_password_hash(password, 10)

    def checkBcrypt(cls, pw_hash, password):
        return cls._bcrypt.check_password_hash(pw_hash, password);
