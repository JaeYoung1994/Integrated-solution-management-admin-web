import json
from flask import request
from flask_restx import Resource, Namespace, fields

from common.utils import Utils
from common.init import Init
from common.socket.tcp.server.tcpServer import TCPServer
from common.utils import Utils


command_check = Namespace(
    name='check',
    description='command state check'
)

@command_check.route('/connect')
class order_check_clients(Resource):
    command_check_clients = command_check.model("order_check_list", {
        "token": fields.String(description="Access Token", required=True, example="token")
    })
    command_check_clients_Error = command_check.model("order_check_list_Error", {
        "result": fields.String(description="Access Token", required=True, example="token")
    })
    @command_check.response(400, "Fail", command_check_clients_Error)
    @command_check.expect(command_check_clients)
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
                rv["result"], code = True, 200
        except Exception as ex:
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}


