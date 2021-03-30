import json
from flask import session
from common.init import Init
from common.utils import Utils

class Session:
    def checkSession(self):
        isSession = False
        if "sessionKey" not in session:
            return isSession
        else:
            method = "POST"
            url = Init.apiPath()+"/auth/user/chk/session"
            j = {
                "token":"1234",
                "session":session["sessionKey"]
            }
            res = Utils.requestUrl(method=method, url=url, json=j)
            if res.status_code == 200:
                j = json.loads(res.text)
                isSession = j['result']
            else:
                del session["sessionKey"]
            return isSession

