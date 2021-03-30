from uuid import uuid4

class Init():
    # restApi 주소
    _initPath = "http://www.shiptroll.com"
    # TCPServerApi 주소
    _commandPath = "http://cmd.shiptroll.com"

    @classmethod
    def getInitPath(cls):
        return cls._initPath

    @classmethod
    def getCommandPath(cls):
        return cls._commandPath


