import copy
import json

from flask import request
from flask_restx import Resource, Namespace, fields

from model.maria.user.userSql import UserSql as MariaUserSql
from model.redis.user.session import Session as RedisSession
from common.security.encryption import Encryption
from common.utils import Utils
from common.code import ReqCode, SignCode, CommonCode

auth_user = Namespace(
    name='auth_user',
    description='User authentication API'
)

@auth_user.route('/signin')
class Auth_user_signin(Resource):
    signin_fields_account = auth_user.model("auth_user_signin_account", {
        "email": fields.String(description="Login Account", required=True, example="User email"),
        "password": fields.String(description="Login Account", required=True, example="User password")
    })

    # signin request json Model
    signin_fields = auth_user.model("auth_user_signin", {
        "token": fields.String(description="Access Token Value", required=True, example="Token value issued"),
        "account": fields.Nested(signin_fields_account)
    })
    # signin response success data Model
    signin_success_data = auth_user.model("auth_user_signin_success_data", {
        "session": fields.String(description="Return created session value", required=True, example="Session value"),
    })
    # signin response success Model
    signin_success = auth_user.model("auth_user_signin_success", {
        "result": fields.String(description="Access Token Value", required=True, example=True),
        "data": fields.Nested(signin_success_data)
    })
    # signin response false Model
    signin_false = auth_user.model("auth_user_signin_false", {
        "result": fields.String(description="result boolean", required=True, example=True),
        "code": fields.String(description="Error Code", required=True, example="Error Code"),
        "msg": fields.String(description="Error message", required=True, example="Error message")
    })

    @auth_user.response(200, "Success", signin_success)
    @auth_user.response(400, "Fail", signin_false)
    @auth_user.expect(signin_fields)
    def post(self):
        """ User sign in API """
        rv, code = {}, 200
        try:
            req = request.json
            hasKey = ["token", "account"]
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
                user = json.dumps({"email":userInfo["data"]["email"]})
                session = RedisSession().createSession(user)
                rv = copy.deepcopy(CommonCode.Success.value)
                rv["data"] = {"session": session}
            else:
                rv, code = SignCode.SignFail.value, 400
        except Exception as ex:
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}

@auth_user.route("/signout")
class Auth_user_signout(Resource):
    # signout request json Model
    signout_fields = auth_user.model("auth_user_signout", {
        "token": fields.String(description="Access Token Value", required=True, example="Access Token Value"),
        "session": fields.String(description="Session Value", required=True, example="Session Value")
    })
    # signout response success Model
    signout_success = auth_user.model("auth_user_signout_success", {
        "result": fields.String(description="Login was successful", required=True, example=True),
    })
    # signout response false Model
    signout_false = auth_user.model("auth_user_signout_false", {
        "result": fields.String(description="result boolean", required=True, example=True),
        "code": fields.String(description="Error Code", required=True, example="Error Code"),
        "msg": fields.String(description="Error message", required=True, example="Error message")
    })
    @auth_user.expect(signout_fields)
    @auth_user.response(200, "Success", signout_success)
    @auth_user.response(400, "Fail", signout_false)
    def post(self):
        """User sign out API"""
        code = 200
        try:
            req = request.json
            hasKey = ["token", "session"]
            isKey = Utils.isDicHasKey(req, hasKey)
            if not isKey:
                return ReqCode.notKey.value, 400
            isNullKey = Utils.isDicKeyValueNull(req, hasKey)
            if not isNullKey:
                return ReqCode.keyValNull.value, 400

            session = req.get("session")
            # Session removal
            RedisSession().deleteSession(session)
            rv = CommonCode.Success.value
        except Exception as ex:
            code = 400
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            rv["msg"] = str(ex)
        return rv, code #, {"hi": "hello"}

@auth_user.route('/chk/session')
class Auth_user_check_Session(Resource):
    # checkSession request json Model
    chk_session_fields = auth_user.model("auth_user_chk_Session", {
        "token": fields.String(description="Access Token Value", required=True, example="Access Token Value"),
        "session": fields.String(description="Session Value", required=True, example="Session Value")
    })
    # checkSession request json Model
    chk_Session_success = auth_user.model("auth_user_chk_Session_success", {
        "result": fields.String(description="Success or not", required=True, example="True or False"),
        "data": fields.String(description="", required=True, example="user dictionary")
    })
    # signout response false Model
    chk_session_false = auth_user.model("auth_user_chk_Session_false", {
        "result": fields.String(description="result boolean", required=True, example=True),
        "code": fields.String(description="Error Code", required=True, example="Error Code"),
        "msg": fields.String(description="Error message", required=True, example="Error message")
    })
    @auth_user.expect(chk_session_fields)
    @auth_user.response(200, "Success", chk_Session_success)
    @auth_user.response(400, "Fail", chk_session_false)
    def post(self):
        """Session Expiration Check API"""
        rv, code = {}, 200
        try:
            req = request.json
            hasKey = ["session"]
            isKey = Utils.isDicHasKey(req, hasKey)
            if not isKey:
                return ReqCode.notKey.value, 400
            isNullKey = Utils.isDicKeyValueNull(req, hasKey)
            if not isNullKey:
                return ReqCode.keyValNull.value, 400

            session = req.get("session")
            # Session validity check
            redisSesson = RedisSession();
            check = redisSesson.checkSession(session)
            if check:
                data = redisSesson.getSession(session)
                rv = {"result":True, "data": json.loads(data)}
            else:
                code = 400
                rv = CommonCode.Fail.value
        except Exception as ex:
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            rv["msg"] = str(ex)
        return rv, code #, {"hi": "hello"}


