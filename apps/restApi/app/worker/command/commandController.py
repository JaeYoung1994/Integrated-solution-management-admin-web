import copy
import json

from flask import request
from flask_restx import Resource, Namespace, fields
from model.redis.worker.command.commandRedis import CommandRedis
from model.redis.worker.client.clientRedis import ClientRedis

from common.utils import Utils
from common.code import ReqCode, CommonCode

ra_worker_command = Namespace(
    name='worker_command',
    description='Worker to Command API'
)

@ra_worker_command.route('/register')
class worker_command_register(Resource):
    # chk_email request json Model
    chk_email_fields = ra_worker_command.model("worker_command_register_email", {
        "token": fields.String(description="Access Token Value", required=True, example="Token value issued")
    })

    # chk_email response success Model
    chk_email_result = ra_worker_command.model("worker_command_register_success", {
        "result": fields.String(description="result boolean", required=True, example=True),
        "code": fields.String(description="result Code", required=True, example="Error Code"),
        "msg": fields.String(description="result message", required=True, example="Error message")
    })
    @ra_worker_command.response(200, "Success", chk_email_result)
    @ra_worker_command.response(400, "Fail", chk_email_result)
    @ra_worker_command.expect(chk_email_fields)
    def post(self):
        """ Check for duplicate emails in API """
        code = 200
        try:
            req = request.json
            # Checking the existence of email in DB (MariaDB)
            rvKey = ['token']
            isKey, isVal = Utils.isDicHasKey(req, rvKey), Utils.isDicKeyValueNull(req, rvKey)
            if not isKey:
                return ReqCode.notKey.value, 400
            if not isVal:
                return ReqCode.keyValNull.value, 400

            ip = request.environ
            if 'HTTP_X_FORWARDED_FOR' in request.environ:
                a = request.environ['HTTP_X_FORWARDED_FOR']
                ip = request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
            if 'REMOTE_ADDR' in request.environ:
                ip = request.list_storage_class([request.environ['REMOTE_ADDR']])[0]

            commandRedis = CommandRedis()
            commandRedis.registCommand(ip, req["token"])
            rv = CommonCode.Success.value
        except Exception as ex:
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}

@ra_worker_command.route('/delete')
class worker_command_delete(Resource):
    # chk_email request json Model
    chk_email_fields = ra_worker_command.model("worker_command_register_email", {
        "token": fields.String(description="Access Token Value", required=True, example="Token value issued")
    })

    # chk_email response success Model
    chk_email_result = ra_worker_command.model("worker_command_register_success", {
        "result": fields.String(description="result boolean", required=True, example=True),
        "code": fields.String(description="result Code", required=True, example="Error Code"),
        "msg": fields.String(description="result message", required=True, example="Error message")
    })
    @ra_worker_command.response(200, "Success", chk_email_result)
    @ra_worker_command.response(400, "Fail", chk_email_result)
    @ra_worker_command.expect(chk_email_fields)
    def post(self):
        """ Check for duplicate emails in API """
        code = 200
        try:
            req = request.json
            # Checking the existence of email in DB (MariaDB)
            rvKey = ['ip']
            isKey, isVal = Utils.isDicHasKey(req, rvKey), Utils.isDicKeyValueNull(req, rvKey)
            if not isKey:
                return ReqCode.notKey.value, 400
            if not isVal:
                return ReqCode.keyValNull.value, 400
            commandRedis = CommandRedis()
            for ip in req['ip']:
                commandRedis.deleteCommand(ip)

            clientRedis = ClientRedis
            clients = ClientRedis.getClient()
            for client in clients:
                if clients[client] in req['ip']:
                    clientRedis.deleteClient(client)

            rv = CommonCode.Success.value
        except Exception as ex:
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}

@ra_worker_command.route('/list')
class worker_command_list(Resource):
    # chk_email request json Model
    chk_email_fields = ra_worker_command.model("worker_command_register_email", {
        "token": fields.String(description="Access Token Value", required=True, example="Token value issued")
    })

    # chk_email response success Model
    chk_email_result = ra_worker_command.model("worker_command_register_success", {
        "result": fields.String(description="result boolean", required=True, example=True),
        "code": fields.String(description="result Code", required=True, example="Error Code"),
        "msg": fields.String(description="result message", required=True, example="Error message")
    })
    @ra_worker_command.response(200, "Success", chk_email_result)
    @ra_worker_command.response(400, "Fail", chk_email_result)
    @ra_worker_command.expect(chk_email_fields)
    def post(self):
        """ Check for duplicate emails in API """
        code = 200
        try:
            req = request.json
            commandRedis = CommandRedis()
            data = commandRedis.getRegistCommand()
            rv = {"result":True, "data":data }
        except Exception as ex:
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}


