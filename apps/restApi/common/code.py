#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
from enum import Enum

class ReqCode(Enum):
    notKey = { "result":False, "code": "E0_001", "msg": "Invalid input value."}
    keyValNull = {"result": False, "code": "E0_001", "msg": "Required value input error"}

class SignCode(Enum):
    SignFail = {"result":False, "code": "E1_001", "msg": "Login failed."}
    NotEmail = {"result":False, "code": "SU_001", "msg": "The account value entered is not an email."}
    ExistEmail = {"result":False, "code": "SU_002", "msg": "Email already registered."}
    ExistNickName = {"result":False, "code": "SU_002", "msg": "NickName already registered."}

class CommonCode(Enum):
    Success = {"result":True }
    Fail = {"result":False }
    UnknownError = {"result":False, "code": "CM_001"}