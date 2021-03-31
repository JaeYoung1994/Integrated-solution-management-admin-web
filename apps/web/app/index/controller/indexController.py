# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, redirect, session
from common.auth.session import Session
from common.auth.menu import Menu
from common.worker.command import Command

from common.init import Init


template_path = Init.tempPath()
api_path = Init.apiPath()
bp_index_index = Blueprint("index_index", __name__, template_folder="/templates")

'''
메인 화면
Main screen
author: 이재영 (Jae Young Lee)
'''
@bp_index_index.route("/")
def index_view():
    # 세션 여부 체크
    userInfo = Session().checkSession()
    if not userInfo["result"]:
        return redirect(url_for("index_sign.signin_view"))

    menu = Menu()
    # 메뉴 권한 확인
    #isMenuAuth = menu.isAuth("/", userInfo["data"])
    #if not isMenuAuth["result"]:
        #return redirect(url_for("index_index.index_view"))

    # 메뉴 html 생성
    menuHtml = menu.list("/", userInfo["data"])

    command = Command()
    # 연결된 TCP Server(Command) 목록
    commands = command.getCommandList()
    # 연결된 TCP Clinet(Worker) 목록
    clients = command.getClientList()
    return render_template(template_path + '/main/index/index.html', menuHtml=menuHtml, clientCnt=len(clients), commands=len(commands))