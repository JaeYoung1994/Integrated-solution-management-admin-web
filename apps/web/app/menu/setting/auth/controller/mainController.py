# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, redirect, request
from common.auth.session import Session
from common.auth.menu import Menu
from common.utils import Utils
from common.init import Init
import json

template_path = Init.tempPath()
api_path = Init.apiPath()
bp_menu_setting_auth_main = Blueprint("menu_setting_auth_main", __name__, template_folder="/templates")

'''
계정 관리 화면
Account management screen
author: 이재영 (Jae Young Lee)
'''
@bp_menu_setting_auth_main.route("/auth")
def menu_setting_auth_view():
    if not Session().checkSession():
        return redirect(url_for('index_sign.signin_view'))
    menu = Menu()
    menuHtml = menu.list("/setting/auth")
    authority = "authority"
    apiUrl = Init.apiPath() + "/user/authority"
    resAuthority = Utils.requestUrl(method="GET", url=apiUrl)
    if resAuthority.status_code == 200:
        resAuthorityJson = json.loads(resAuthority.text)
    if resAuthorityJson["result"]:
        authoritys = resAuthorityJson["data"]
    else:
        authoritys = None
    return render_template(template_path + '/main/menu/setting/auth.html', menuHtml=menuHtml, authoritys=authoritys)

'''
계정 관리 화면
Account management screen
author: 이재영 (Jae Young Lee)
'''
@bp_menu_setting_auth_main.route("/auth/register", methods =['POST'])
def menu_setting_auth_register_ajax():
    if not Session().checkSession():
        return redirect(url_for('index_sign.signin_view'))
    result = {"result": False, "msg": "아이디 혹은 패스워드를 확인해주세요."}
    j = {
        "token":"123",
        "account":request.json
    }
    print(request.json)
    method = "POST"
    url = Init.apiPath() +"/user/register"
    resApi = Utils.requestUrl(method=method, url=url, json=j)

    if resApi.status_code == 200:
        result = {"result": True}
    return json.dumps(result);