# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, redirect
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
    if not Session().checkSession():
        return redirect(url_for('index_sign.signin_view'))
    menu = Menu()
    command = Command()
    clients = command.getClientList()
    commands = command.getCommandList()
    menuHtml = menu.list("/")
    return render_template(template_path + '/main/index/index.html', menuHtml=menuHtml, clientCnt=len(clients), commands=len(commands))