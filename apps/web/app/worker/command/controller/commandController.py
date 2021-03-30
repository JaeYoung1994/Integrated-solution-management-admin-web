# -*- coding: utf-8 -*-
import json
from flask import Blueprint, url_for, redirect, request

from common.auth.session import Session
from common.worker.command import Command
from common.init import Init
from uuid import uuid4

template_path = Init.tempPath()
bp_client_command = Blueprint("client_command", __name__, template_folder="/templates")

@bp_client_command.route("/get/list", methods =['POST'])
def client_command_get_clients_list():
    if not Session().checkSession():
        return redirect(url_for('index_sign.signin_view'))
    command = Command()
    clients = command.getClientList()
    result = {"result": True, "data":clients}
    return json.dumps(result)

@bp_client_command.route("/req/sync", methods =['POST'])
def client_command_sync_commnad():
    if not Session().checkSession():
        return redirect(url_for('index_sign.signin_view'))
    command = Command()
    commands = command.syncCommands()
    result = {"result": True, "data":len(commands)}
    return json.dumps(result)