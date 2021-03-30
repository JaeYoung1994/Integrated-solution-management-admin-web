class Init():
    restApiPath = "http://127.0.0.1:5000"
    templatePath = "/001"
    sessionDic = "123"
    commandPort = "9000"

    @classmethod
    def sessionDic(cls):
        return cls.sessionDic

    @classmethod
    def tempPath(cls):
        return cls.templatePath

    @classmethod
    def apiPath(cls):
        return cls.restApiPath

    @classmethod
    def getCommandPort(cls):
        return cls.commandPort

