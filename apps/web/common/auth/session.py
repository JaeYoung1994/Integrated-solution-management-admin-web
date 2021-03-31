import json
from flask import session
from common.init import Init
from common.utils import Utils

class Session:
    def checkSession(self):
        result = {"result": False}
        if "sessionKey" not in session:
            return result
        else:
            method = "POST"
            url = Init.apiPath()+"/auth/user/chk/session"
            j = {
                "session":session["sessionKey"]
            }
            res = Utils.requestUrl(method=method, url=url, json=j)
            if res.status_code == 200:
                result = json.loads(res.text)
            else:
                del session["sessionKey"]
            return result

