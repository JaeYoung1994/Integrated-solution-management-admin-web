import copy

from flask import request
from flask_restx import Resource, Namespace, fields
from model.maria.sys.main.sysMainSql import SysMainSql
from model.maria.user.userSql import UserSql
from model.redis.user.session import Session as RedisSession



sys_main_menu = Namespace(
    name='sys_main_menu',
    description='User API'
)

@sys_main_menu.route('/menu')
class data_user_chk_email(Resource):
    # get main_menu list api require json Model
    sys_menu_fields = sys_main_menu.model("sys_main_menu_req", {
        "session": fields.String(description="Access Token Value", required=True, example="Token value issued")
    })

    # get main_menu list api return for json success Model
    sys_menu_success_return = sys_main_menu.model("sys_main_menu_return", {
        "result": fields.String(description="result boolean", required=True, example=True),
        "code": fields.String(description="result Code", required=True, example="Error Code"),
        "msg": fields.String(description="result message", required=True, example="Error message")
    })


    @sys_main_menu.response(200, "Success", sys_menu_success_return)
    @sys_main_menu.response(400, "Fail", sys_menu_success_return)
    def post(self):
        """ Check for duplicate emails in API """
        code = 200
        try:
            req = request.json
            # Checking the existence of email in DB (MariaDB)
            rvUser = UserSql().getAccountInfo(user = req)

            if rvUser['result']:
                rvMenu = SysMainSql().getMainMenuList(authCode = rvUser['data']['authority'], groupCode = rvUser['data']['group'])
                if rvMenu['result']:
                    res = {"result": True, "code": "E0_000", "data":rvMenu['data']}
                else:
                    res = rvMenu
        except Exception as ex:
            res = {"result": False, "msg":str(ex), "code": "CM_001"}
            code = 400
        return res, code