# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, session
import json

from common.utils import Utils
from common.init import Init

template_path = Init.tempPath()
bp_index_sign = Blueprint("index_sign", __name__, template_folder="/templates")

'''
로그인 화면
Login screen
author: 이재영 (Jae Young Lee)
'''
@bp_index_sign.route("/signin")
def signin_view():
    return render_template(template_path + '/main/index/auth/signIn.html')

'''
로그인 Ajax
SignIn Ajax
author: 이재영 (Jae Young Lee)
'''
@bp_index_sign.route("/signin.do", methods =['POST'])
def signin_ajax():
    result = {"result": False, "msg": "아이디 혹은 패스워드를 확인해주세요."}
    j = {
        "token":"123",
        "account":request.json
    }
    method = "POST"
    url = Init.apiPath() +"/auth/user/signin"
    resLogin = Utils.requestUrl(method=method, url=url, json=j)

    if resLogin.status_code == 200:
        loginJson = json.loads(resLogin.text)
        if loginJson["result"]:
            session["sessionKey"] = loginJson["data"]["session"]
            result["result"] = True
            del result["msg"]
    return json.dumps(result);

'''
로그아웃 ajax
Sign Out ajax
author: 이재영 (Jae Young Lee)
'''
@bp_index_sign.route("/signout.do", methods =['POST'])
def signout_ajax():
    result = {"result": False, "msg": "로그아웃에 실패하였습니다."}
    j = {
        "token":"123",
        "session":session["sessionKey"]
    }
    method = "POST"
    url = Init.apiPath() +"/auth/user/signout"
    resSignout = Utils.requestUrl(method=method, url=url, json=j)

    if resSignout.status_code == 200:
        loginJson = json.loads(resSignout.text)
        if loginJson["result"]:
            result["result"] = True
            del result["msg"]
    return json.dumps(result);