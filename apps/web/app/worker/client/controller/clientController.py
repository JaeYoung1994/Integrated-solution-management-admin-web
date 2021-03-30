# -*- coding: utf-8 -*-
import json
from flask import Blueprint, request, redirect, url_for
from common.auth.session import Session
from common.worker.command import Command
from uuid import uuid4

bp_worker_client = Blueprint("worker_client", __name__, template_folder="/templates")

@bp_worker_client.route("/authKey", methods = ['GET'])
def worker_client_authkey():
    # 추 후 client ip 체크 기능 추가
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    token = str(uuid4())
    result = {
        "ip":ip
    }
    print(result)
    return json.dumps(result)

@bp_worker_client.route("/req/sync", methods =['POST'])
def client_command_sync_clients():
    if not Session().checkSession():
        return redirect(url_for('index_sign.signin_view'))
    command = Command()
    command.syncClinetCount()
    result = {"result": True}
    return json.dumps(result)

@bp_worker_client.route("/req/sync/device", methods =['POST'])
def client_command_sync_clients_device():
    if not Session().checkSession():
        return redirect(url_for('index_sign.signin_view'))
    command = Command()
    command.syncClinetCount()
    result = {"result": True}
    return json.dumps(result)


@bp_worker_client.route("/get/list", methods =['POST'])
def client_command_get_command_to_client_list():
    if not Session().checkSession():
        return redirect(url_for('index_sign.signin_view'))
    command = Command()
    clients = command.getClientList()
    commands = command.getCommandList()

    connectToClient = {}
    for server in commands:
        connectToClient[server] = 0

    for client in clients:
        if clients[client] in list(connectToClient.keys()):
            connectToClient[clients[client]] = connectToClient[clients[client]] + 1

    result = {"result": True, "data":connectToClient}
    return json.dumps(result)

