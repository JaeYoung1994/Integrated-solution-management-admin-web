import json
from flask import request
from flask_restx import Resource, Namespace, fields

from common.utils import Utils
from common.init import Init
from common.socket.tcp.server.tcpServer import TCPServer
from common.utils import Utils

order_check = Namespace(
    name='order',
    description='User authentication API'
)

@order_check.route('/clients')
class order_check_clients(Resource):
    order_check_clients = order_check.model("order_check_list", {
        "token": fields.String(description="Access Token", required=True, example="token")
    })
    order_check_clients_Error = order_check.model("order_check_list_Error", {
        "result": fields.String(description="Access Token", required=True, example="token")
    })
    @order_check.response(400, "Fail", order_check_clients_Error)
    @order_check.expect(order_check_clients)
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
                clients = tcpServer.getClients()

                data = []
                for client in clients:
                    data.append(client)

                url = Init.getApiPath()+"/worker/client/sync/clients"
                j = {"data":data}
                res = Utils.requestUrl(method="POST", url=url, json =j)
                rv["result"], code = True, 200
        except Exception as ex:
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}

@order_check.route('/clients/device')
class order_check_clients_device(Resource):
    order_check_clients = order_check.model("order_check_list", {
        "token": fields.String(description="Access Token", required=True, example="token")
    })

    order_check_clients_Error = order_check.model("order_check_list_Error", {
        "result": fields.String(description="Access Token", required=True, example="token")
    })
    @order_check.response(400, "Fail", order_check_clients_Error)
    @order_check.expect(order_check_clients)
    def post(self):
        """ User sign in API """
        rv, code = { "result":False }, 400
        try:
            req = request.json
            hasKey = ["token"]
            isKey = Utils.isDicHasKey(req, hasKey)
            if not isKey:
                return rv, code

            if not req["token"] == Init.getToken():
                return rv, code
            else:
                msg = {'job':'sync_system_status'}
                tcpServer = TCPServer()
                tcpServer.sendMessageToAll(json.dumps(msg))
                rv["result"], code = True, 200
        except Exception as ex:
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}


