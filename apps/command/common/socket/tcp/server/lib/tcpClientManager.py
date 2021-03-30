#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
from common.socket.tcp.server.lib.tcpClient import TCPClient

'''
소켓 통신 접속 유저 관리 및 메시지 보내기
'''
class TCPClientManager:
    def __init__(self):
        self.tcpClient = TCPClient()
         
    def addClient(self, client_name, conn, addr):

        if client_name in self.tcpClient.getClients():
            conn.send('이미 등록된 사용자입니다.\n'.encode())
            conn.close()
            return
        # 새로운 사용자를 등록함
        self.tcpClient.addClient(client_name, conn, addr)
        print('+++ 클라이언트 접속 [%s] 총 연결 [%d]' % (client_name, len(self.tcpClient.getClients())))
        return client_name
 
    def removeClient(self, client_name):
        if client_name not in self.tcpClient.getClients():
            return
        self.tcpClient.delClient(client_name)
        print('--- 대화 참여자 수 [%d]' % len(self.tcpClient.getClients()))
 
    def messageHandler(self, client_name, msg):
        if len(msg) == 0:
            return
        
        if msg[0] != '/':
            return

        if msg.strip() == '/quit':
            self.removeUser(client_name)
            return -1