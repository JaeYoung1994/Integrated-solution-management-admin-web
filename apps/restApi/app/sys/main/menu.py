import copy

from flask import request
from flask_restx import Resource, Namespace, fields
from model.maria.sys.main.sysMainSql import SysMainSql



sys_main_menu = Namespace(
    name='sys_main_menu',
    description='User API'
)

@sys_main_menu.route('/menu')
class data_user_chk_email(Resource):
    # get main_menu list api require json Model
    sys_menu_fields = sys_main_menu.model("sys_main_menu_req", {
        "token": fields.String(description="Access Token Value", required=True, example="Token value issued")
    })

    # get main_menu list api return for json success Model
    sys_menu_success_return = sys_main_menu.model("sys_main_menu_return", {
        "result": fields.String(description="result boolean", required=True, example=True),
        "code": fields.String(description="result Code", required=True, example="Error Code"),
        "msg": fields.String(description="result message", required=True, example="Error message")
    })


    @sys_main_menu.response(200, "Success", sys_menu_success_return)
    @sys_main_menu.response(400, "Fail", sys_menu_success_return)
    def get(self):
        """ Check for duplicate emails in API """
        code = 200
        try:
            req = request.json
            # Checking the existence of email in DB (MariaDB)
            mariaDB = SysMainSql()
            rv = mariaDB.getMainMenuList()
            if rv['result']:
                res = {"result": True, "code": "E0_000", "data":rv['data']}
        except Exception as ex:
            res = {"result": False, "code": "CM_001"}
            rv["msg"] = str(ex)
            code = 400
        return res, code