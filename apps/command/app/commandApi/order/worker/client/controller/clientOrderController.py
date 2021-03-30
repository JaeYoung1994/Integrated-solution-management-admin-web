import json
from flask import request
from flask_restx import Resource, Namespace, fields

from common.utils import Utils
from common.init import Init
from common.socket.tcp.server.tcpServer import TCPServer
from common.utils import Utils


order_worker_client_clientOrder_check = Namespace(
    name='worker_client_clientOrder',
    description='client 정보 관련 API'
)

'''
디바이스 정보 동기화
'''
@order_worker_client_clientOrder_check.route('/sync/system')
class order_check_clients(Resource):
    order_worker = order_worker_client_clientOrder_check.model("order_worker_client_clientOrder_check_sync_system", {
        "token": fields.String(description="Access Token", required=True, example="token")
    })
    @order_worker_client_clientOrder_check.response(400, "Fail", order_worker)
    @order_worker_client_clientOrder_check.expect(order_worker)
    def post(self):
        """ User sign in API """
        rv, code = {"result":False}, 400
        try:
            req = request.json
            hasKey = ["token"]
            isKey = Utils.isDicHasKey(req, hasKey)
            if not isKey:
                return rv, code

            if not req["token"] == Init.getToken():
                return rv, code
            else:
                tcpServer = TCPServer()
                clients = tcpServer
                msg = {'job': 'sync_system'}
                tcpServer.sendMessageToAll(json.dumps(msg))
                rv["result"], code = True, 200
        except Exception as ex:
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}


