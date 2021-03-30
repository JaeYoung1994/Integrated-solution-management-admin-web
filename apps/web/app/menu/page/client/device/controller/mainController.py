# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, redirect, request
from common.auth.session import Session
from common.auth.menu import Menu
from common.worker.command import Command
from common.utils import Utils
from common.init import Init
import json

template_path = Init.tempPath()
api_path = Init.apiPath()
bp_menu_page_client_device_main = Blueprint("menu_page_client_device_main", __name__, template_folder="/templates")

'''
디바이스 화면
Device screen
author: 이재영 (Jae Young Lee)
'''
@bp_menu_page_client_device_main.route("/")
def menu_page_client_device_view():
    if not Session().checkSession():
        return redirect(url_for('index_sign.signin_view'))
    menu = Menu()
    menuHtml = menu.list("/client/device")
    authority = "authority"
    apiUrl = Init.apiPath() + "/user/authority"
    resAuthority = Utils.requestUrl(method="GET", url=apiUrl)
    if resAuthority.status_code == 200:
        resAuthorityJson = json.loads(resAuthority.text)
    if resAuthorityJson["result"]:
        authoritys = resAuthorityJson["data"]
    else:
        authoritys = None
    return render_template(template_path + '/main/menu/pages/client/device.html', menuHtml=menuHtml, authoritys=authoritys)

'''
클라이언트 서버 정보
Clinet Server Info
author: 이재영 (Jae Young Lee)
'''
@bp_menu_page_client_device_main.route("/get/list", methods =['POST'])
def menu_page_client_device_get_list():
    if not Session().checkSession():
        return redirect(url_for('index_sign.signin_view'))
    command = Command()
    command.syncClientDeviceList()
    clients = command.getClientDeviceList()
    result = {"result": True, "data":clients}
    return json.dumps(result)
