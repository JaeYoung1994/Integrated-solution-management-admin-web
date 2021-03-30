import copy
from flask import request
from flask_restx import Resource, Namespace, fields

from common.utils import Utils

order_crwaler = Namespace(
    name='crwaler',
    description='User authentication API'
)

@order_crwaler.route('/crwaler')
class Order_Crwaler(Resource):
    signin_fields_account = order.model("order_crwaler", {
        "token": fields.String(description="Access Token", required=True, example="token"),
        "jobName": fields.String(description="Login Account", required=True, example="JobName"),
        "param": fields.String(description="json to String", required=True, example="JobName")
    })

    def post(self):
        """ User sign in API """
        rv, code = {}, 201
        try:
            req = request.json
            hasKey = ["token", "jobName", "param"]
            isKey = Utils.isDicHasKey(req, hasKey)
            if not isKey:
                return ReqCode.notKey.value, 400
            isNullKey = Utils.isDicKeyValueNull(req, hasKey)
            if not isNullKey:
                return ReqCode.keyValNull.value, 400
            hasKey = ["email", "password"]
            isKey = Utils.isDicHasKey(req["account"], hasKey)
            if not isKey:
                return ReqCode.notKey.value, 400
            isNullKey = Utils.isDicKeyValueNull(req["account"], hasKey)
            if not isNullKey:
                return ReqCode.keyValNull.value, 400

            # Import user information from MariaDB
            account = req["account"]
            userInfo = MariaUserSql().getAccountInfo(account);
            if not userInfo['result']:
                rv = CommonCode.UnknownError.value
                rv = userInfo['msg']
                return rv, 400

            if userInfo['data'] is None:
                return SignCode.SignFail.value, 400

            # if userInfo[''] is null:
            pwdChk = Encryption().checkBcrypt(userInfo["data"]["password"], account["password"])

            # Create session if passwords match
            if pwdChk:
                session = RedisSession().createSession(userInfo["data"]["email"])
                rv = copy.deepcopy(CommonCode.Success.value)
                rv["data"] = {"session": session}
            else:
                rv, code = SignCode.SignFail.value, 400
        except Exception as ex:
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}


