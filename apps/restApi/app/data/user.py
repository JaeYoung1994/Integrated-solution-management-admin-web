import copy

from flask import request
from flask_restx import Resource, Namespace, fields
from model.maria.user.userSql import UserSql as MariaUserSql
from common.security.encryption import Encryption
from common.utils import Utils
from common.code import ReqCode, SignCode, CommonCode

data_user = Namespace(
    name='data_user',
    description='User API'
)

@data_user.route('/chk/email')
class data_user_chk_email(Resource):
    # chk_email request json Model
    chk_email_fields = data_user.model("data_user_chk_email", {
        "token": fields.String(description="Access Token Value", required=True, example="Token value issued"),
        "email": fields.String(description="Login Account", required=True, example="User email")
    })

    # chk_email response success Model
    chk_email_result = data_user.model("data_user_chk_email_success", {
        "result": fields.String(description="result boolean", required=True, example=True),
        "code": fields.String(description="result Code", required=True, example="Error Code"),
        "msg": fields.String(description="result message", required=True, example="Error message")
    })
    @data_user.response(200, "Success", chk_email_result)
    @data_user.response(400, "Fail", chk_email_result)
    @data_user.expect(chk_email_fields)
    def post(self):
        """ Check for duplicate emails in API """
        code = 200
        try:
            req = request.json
            # Checking the existence of email in DB (MariaDB)
            mariaUserSql = MariaUserSql()
            chkEmail = mariaUserSql.isEmail(req);
            if not chkEmail:
                rv = SignCode.NotEmail.value
                return rv, code

            # Check for duplicate emails
            chkEmail = mariaUserSql.isEmail(req)
            if not chkEmail['result']:
                rv = SignCode.ExistEmail.value
                return rv, code
            rv = CommonCode.Success.value

        except Exception as ex:
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}

@data_user.route('/chk/nickname')
class data_user_chk_nickname(Resource):
    # chk_email request json Model
    chk_nickname_fields = data_user.model("data_user_chk_nickname", {
        "token": fields.String(description="Access Token Value", required=True, example="Token value issued"),
        "nickName": fields.String(description="Login Account", required=True, example="User email")
    })
    # chk_email response false Model
    chk_nickname_result = data_user.model("data_user_chk_nickname_error", {
        "result": fields.String(description="result boolean", required=True, example=True),
        "code": fields.String(description="result Code", required=True, example="Error Code"),
        "msg": fields.String(description="result message", required=True, example="Error message")
    })
    @data_user.response(200, "Success", chk_nickname_result)
    @data_user.response(400, "Fail", chk_nickname_result)
    @data_user.expect(chk_nickname_fields)
    def post(self):
        """ Check for duplicate nickname in API """
        code = 200
        try:
            req = request.json
            # Checking the existence of nickname in DB (MariaDB)
            mariaUserSql = MariaUserSql()
            # Check for duplicate nickname
            chkNickName = mariaUserSql.isNickName(req)
            if not chkNickName['result']:
                rv = SignCode.ExistNickName.value
                return rv, code
            rv = CommonCode.Success.value
        except Exception as ex:
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            rv["msg"] = str(ex)
            code = 400
        return rv, code  # ,header{"hi": "hello"}

@data_user.route('/register')
class data_user_register(Resource):
    # register request json Model
    register_fields_userInfo = data_user.model("data_user_register_userInfo", {
        "email": fields.String(description="User email to register", required=True, example="email value"),
        "nickName": fields.String(description="User nickname to register", required=True, example="nickname value"),
        "password": fields.String(description="User password to register", required=True, example="password value"),
        "firstName": fields.String(description="User firstName to register", required=True, example="firstName value"),
        "lastName": fields.String(description="User lastName to register", required=True, example="lastName value"),
        "authority": fields.String(description="User authority to register", required=True, example="authority value")
    })
    register_fields = data_user.model("data_user_register", {
        "token": fields.String(description="Access Token Value", required=True, example="Token value issued"),
        "account": fields.Nested(register_fields_userInfo)
    })

    # register response success Model
    register_result = data_user.model("data_user_register_success", {
        "result": fields.String(description="result boolean", required=True, example=True),
        "code": fields.String(description="result Code", required=True, example="Error Code"),
        "msg": fields.String(description="result message", required=True, example="Error message")
    })

    @data_user.response(200, "Success", register_result)
    @data_user.response(400, "Fail", register_result)
    @data_user.expect(register_fields)
    def post(self):
        """ User registration API """
        try:
            # Request data check
            req = request.json
            rvKey, rvAccountKey  = ['token', 'account'], ['email', 'nickName', 'password', 'firstName', 'lastName', 'authority']
            isKey, isVal = Utils.isDicHasKey(req, rvKey), Utils.isDicKeyValueNull(req, rvKey)
            if isKey and isVal:
                isKey, isVal = Utils.isDicHasKey(req['account'], rvAccountKey), Utils.isDicKeyValueNull(req['account'], rvAccountKey)

            if not isKey:
                return ReqCode.notKey.value, 400
            if not isVal:
                return ReqCode.keyValNull.value, 400

            account = req['account']
            mariaUserSql = MariaUserSql()

            # Check if it's an email or not
            chkEmail = Utils.isEmail(account['email']);
            if not chkEmail:
                return SignCode.NotEmail.value, 400

            # Check for duplicate emails
            chkEmail = mariaUserSql.isEmail(account)
            if not chkEmail['result']:
                return SignCode.ExistEmail.value, 400

            # Check for duplicate nickname
            chkNickName = mariaUserSql.isNickName(account)
            if not chkNickName['result']:
                return SignCode.ExistNickName.value, 400

            account['password'] = Encryption().changeBcrypt(account['password']).decode('ascii')
            # Checking the existence of nickname in DB (MariaDB)
            chk = mariaUserSql.setAccountRegist(req['account'])
            if chk['result']:
                rv = CommonCode.Success.value
                code = 200
            else:
                rv = copy.deepcopy(CommonCode.UnknownError.value)
                rv['msg'] = chk['msg']
        except Exception as ex:
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            code = 400
        return rv, code  # ,header{"hi": "hello"}


@data_user.route('/authority')
class data_user_authority(Resource):
    # register response success Model
    authority_result = data_user.model("data_user_register_success", {
        "result": fields.String(description="result boolean", required=True, example=True),
        "code": fields.String(description="result Code", required=True, example="Error Code"),
        "msg": fields.String(description="result message", required=True, example="Error message")
    })

    @data_user.response(200, "Success", authority_result)
    def get(self):
        """ User registration API """
        try:
            mariaUserSql = MariaUserSql()
            apiRes = mariaUserSql.getAuthorityList()
            if apiRes["result"]:
                rv = copy.deepcopy(CommonCode.Success.value)
                rv["data"] = apiRes["data"]
                code = 200
        except Exception as ex:
            rv = copy.deepcopy(CommonCode.UnknownError.value)
            code = 400
        return rv, code  # ,header{"hi": "hello"}