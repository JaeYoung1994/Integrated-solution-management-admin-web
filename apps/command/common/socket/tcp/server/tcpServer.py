#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
import socketserver
import socket

from common.socket.tcp.server.lib.tcpHandler import TCPHandler
from common.socket.tcp.server.lib.tcpClient import TCPClient

class TCPManagerServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class TCPServer:
    _instance = None
    _server = None
    _tcpClient = None
    # 단 한번만 생성됨 (통합 컨트롤을 하기 위해 1회만 생성)
    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls._tcpClient = TCPClient()
        return cls._instance

    '''TCP 서버 생성 '''
    def runServer(cls, port):
        print('관리 서버 실행.')
        ip = socket.gethostbyname(socket.gethostname())
        cls._server = TCPManagerServer((ip, port), TCPHandler)
        cls._server.serve_forever()

    def getClients(cls):
        ''' 유저 목록 리스트 '''
        return cls._tcpClient.getClients()

    def getClientsInfo(cls):
        ''' 유저 목록 리스트 '''
        return cls._tcpClient.getClientsInfo()

    def setClientsInfo(cls, client_name, data):
        cls._tcpClient.setClientsInfo(client_name, data)

    def getClient(cls, client_name):
        if client_name not in cls.getClients():
            print(client_name + "(은)는 연결되어 있지 않습니다.")
            return None

        ''' 특정 유저 추출 '''
        user = cls.getClients()[client_name]
        return user

    def sendMessageTarget(cls, msg, client_name):
        ''' 특정 계정에 메시지 보내기 '''
        conn, addr = cls.getClient(client_name)
        conn.send(msg.encode())

    def sendMessageToAll(self, msg):
        ''' 특정 계정에 메시지 보내기 '''
        for conn, addr in self.getClients().values():
            conn.send(msg.encode())

    def exit(self):
        ''' 서버 종료  추가 작업 필요 '''
        self.server.shutdown()
        self.server.server_close()