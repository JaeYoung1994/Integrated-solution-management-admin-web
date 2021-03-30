import json
import time

from flask import request
from flask_restx import Resource, Namespace, fields

from common.utils import Utils
from common.init import Init
from common.socket.tcp.server.tcpServer import TCPServer
from common.utils import Utils


ra_command_sync_client_device = Namespace(
    name='sync_client_device',
    description='User authentication API'
)

@ra_command_sync_client_device.route('/info')
class save_client_device(Resource):
    save_client_device_sync_req_data_store_fields = ra_command_sync_client_device.model("save_client_device_sync_req_data_store_fields", {
        "name": fields.String(description="partition name", required=True, example="")
        , "total": fields.Integer(description="Total partition capacity", required=True, example="")
        , "used": fields.Integer(description="The capacity the partition is using", required=True, example="")
        , "free": fields.Integer(description="The available capacity of the partition", required=True, example="")
        , "percent": fields.String(description="Percentage of total partition usage", required=True, example="")
    })

    save_client_device_sync_req_data_service_fields = ra_command_sync_client_device.model("save_client_device_sync_req_data_service_fields", {
        "name": fields.String(description="service name", required=True, example="")
        ,"desc": fields.String(description="Service description", required=True, example="")
        ,"status": fields.String(description="Service status", required=True, example="")
        ,"startType": fields.String(description="Service Startup Type", required=True, example="")
        ,"logon": fields.String(description="Service owner", required=True, example="")
    })

    save_client_device_sync_req_data_taskscheduler_fields = ra_command_sync_client_device.model("save_client_device_sync_req_data_taskscheduler_fields", {
        "name": fields.String(description="Task scheduler name", required=True, example="")
        , "path": fields.String(description="Task scheduler path", required=True, example="")
        , "status": fields.String(description="Task scheduler status", required=True, example="")
        , "lastRunTime": fields.String(description="Task scheduler last run time", required=True, example="")
        , "lastResult": fields.String(description="Task scheduler last execution result value", required=True, example="")
    })

    save_client_device_sync_req_data_fields = ra_command_sync_client_device.model("save_client_device_sync_req_data_fields",{
        "store": fields.Nested(save_client_device_sync_req_data_store_fields)
        , "service": fields.Nested(save_client_device_sync_req_data_service_fields)
        , "taskscheduler": fields.Nested(save_client_device_sync_req_data_taskscheduler_fields)
    })

    save_client_device_sync_req = ra_command_sync_client_device.model("save_client_device_sync_req", {
        "token":fields.String(description="regist Key", required=True, example="token")
        , "data": fields.Nested(save_client_device_sync_req_data_fields)
    })

    #@ra_save_client_device.response(400, "Fail", order_check_clients_Error)
    @ra_command_sync_client_device.expect(save_client_device_sync_req)
    def post(self):
        """ User sign in API """
        rv, code = {"result":False}, 400
        try:
            # 값 존재 여부 확인
            req = request.json
            rvKey = ['ip', 'data']
            isKey, isVal = Utils.isDicHasKey(req, rvKey), Utils.isDicKeyValueNull(req, rvKey)
            if not(isKey and isVal):
                return rv, code
            webUrl = Init.getWebPath()
            apiPath = Init.getApiPath()
            # Client 정보 최신화
            res = Utils.requestUrl(method="POST", url=webUrl+"/worker/client/sync/device")
            url = Init.getApiPath()+"/worker/client/sync/clients/device"
            j = req
            res = Utils.requestUrl(method="POST", url=url, json=j)
            rv["result"], code = True, 200
        except Exception as ex:
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}



