from uuid import uuid4

class Init():
    # restApi 주소
    _restApiPath = "http://192.168.219.102"
    # 웹 주소
    _webPath = "http://127.0.0.1"
    # 토큰 생성
    _token = str(uuid4())

    @classmethod
    def getApiPath(cls):
        return cls._restApiPath

    @classmethod
    def getWebPath(cls):
        return cls._webPath

    @classmethod
    def getToken(cls):
        return cls._token
