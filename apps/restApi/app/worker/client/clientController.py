import copy

from flask import request
from flask_restx import Resource, Namespace, fields
from model.redis.worker.client.clientRedis import ClientRedis
from common.utils import Utils
from common.code import ReqCode, CommonCode

ra_worker_client = Namespace(
    name='worker_client',
    description='Worker to client API'
)

@ra_worker_client.route('/sync/clients')
class worker_client_sync_clients(Resource):
    def post(self):
        """ Check for duplicate emails in API """
        code = 200
        try:
            req = request.json
            rvKey = ['data']
            isKey = Utils.isDicHasKey(req, rvKey)
            if not isKey:
                return ReqCode.notKey.value, 400

            commandIp = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            clientRedis = ClientRedis()

            clients = clientRedis.getClient()
            connectList = []
            for client in clients:
                if clients[client] == commandIp:
                    connectList.append(client)

            for conncetIp in connectList:
                if conncetIp not in req['data']:
                    clientRedis.deleteClient(conncetIp)

            for clientIp in req['data']:
                clientRedis.registClient(commandIp, clientIp)
            rv = { "result":True }
        except Exception as ex:
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}

@ra_worker_client.route('/get/clients')
class worker_client_get_clients(Resource):
    def post(self):
        """ Check for duplicate emails in API """
        code = 200
        try:
            req = request.json
            clientRedis = ClientRedis()
            clients = clientRedis.getClient()
            rv = { "result":True, "data":clients}
        except Exception as ex:
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}

@ra_worker_client.route('/sync/clients/device')
class worker_client_sync_device(Resource):
    def post(self):
        """ Check for duplicate emails in API """
        code = 200
        try:
            # 값 존재 여부 확인
            req = request.json
            rvKey = ['ip', 'data']
            isKey, isVal = Utils.isDicHasKey(req, rvKey), Utils.isDicKeyValueNull(req, rvKey)
            if not isKey:
                return ReqCode.notKey.value, 400
            if not isVal:
                return ReqCode.keyValNull.value, 400

            clientRedis = ClientRedis()
            clientRedis.registClientDevice(req['ip'], req['data'])
            rv = CommonCode.Success.value
        except Exception as ex:
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}

@ra_worker_client.route('/get/clients/device')
class worker_client_get_clients_device(Resource):
    def post(self):
        """ Check for duplicate emails in API """
        code = 200
        try:
            req = request.json
            clientRedis = ClientRedis()
            clients = clientRedis.getClientDevice()
            rv = {"result": True, "data": clients}
        except Exception as ex:
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}






