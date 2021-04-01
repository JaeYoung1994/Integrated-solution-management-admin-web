from uuid import uuid4

class Init():
    # web 주소
    _initPath = "http://127.0.0.1"
    # TCPServerApi 주소
    _commandPath = "http://127.0.0.1:9000"

    # TCPSever 주소
    _host = '192.168.219.102'
    _port = 9009


    @classmethod
    def getInitPath(cls):
        return cls._initPath

    @classmethod
    def getCommandPath(cls):
        return cls._commandPath

    @classmethod
    def getHost(cls):
        return cls._host

    @classmethod
    def getPort(cls):
        return cls._port
