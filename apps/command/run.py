import time
from flask import Flask
from flask_restx import Api

from app.commandApi.order.check.controller.stateController import order_check
from app.commandApi.command.check.controller.stateController import command_check
from app.commandApi.order.worker.client.controller.clientOrderController import order_worker_client_clientOrder_check
from app.commandApi.command.sync.client.controller.deviceController import ra_command_sync_client_device

from common.thread.threadDev import ThreadDev
from common.socket.tcp.server.tcpServer import TCPServer
from common.init import Init
from common.utils import Utils


app = Flask(__name__)
api = Api(
    app,
    version='command_dev_0.1',
    title='Command processing API',
    description='Work progress related',
    terms_url="/",
    contact="shiptroll@gmail.com",
    license="MIT",
    url_scheme='http'
)
api.add_namespace(order_check, '/order/check')
api.add_namespace(command_check, '/command/check')
api.add_namespace(command_check, '/client/check')
api.add_namespace(order_worker_client_clientOrder_check, '/order/client')
api.add_namespace(ra_command_sync_client_device, '/save/client/device')

'''
TCP 서버 정보 저장
author: 이재영 (Jae Young Lee)
'''
def registerApi(timer):
    while True:
        token = Init.getToken()
        print(Init.getToken())
        url = Init.getApiPath() + "/worker/command/register"
        j = { "token":token }
        resApi = Utils.requestUrl(method="POST", url=url, json=j)
        if resApi.status_code == 200:
            result = { "result": True }
        else:
            result = { "result": False }
        time.sleep(timer)
    return result

'''
main 함수
author: 이재영 (Jae Young Lee)
'''
if __name__ == "__main__":
    # 서버 종료 여부 체크 함수
    restartTime = 5
    # 공통 쓰레드 모듈 실행
    t = ThreadDev()

    # Command 등록 -- 추가 개발 필요
    t.run('register', registerApi, (60*10,))
    # TCP Server 함수 호출
    tcpServer = TCPServer()

    # 서버가 종료 되었을 경우 재시작
    while True:
        # 소켓 서버 종료시 재실행
        if not t.alive('socket'):
            t.run('socket', tcpServer.runServer, (9009,))
        # 웹 서버 종료시 재실행
        if not t.alive('web'):
            t.run('web', app.run, ("0.0.0.0", 9000))
        # 5초 마다 체크
        time.sleep(restartTime)