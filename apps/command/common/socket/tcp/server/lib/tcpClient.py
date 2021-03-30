#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
"""
=====
TCP/IP Server
싱글톤 패턴  TCP 접속 유저 저장
=====
"""
class TCPClient:
    _instance = None
    _client = None
    _client_device = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls._client = {}
            cls._client_device = {}
        return cls._instance

    def getClients(cls):
        return cls._client

    def getClientsInfo(cls):
        return cls._client_device

    def setClientsInfo(cls, client_name, data):
        if cls._client.get(client_name):
            cls._client_device[client_name] = data

    def addClient(cls, client_name, conn, addr):
        '''TCP 접근 유저 추가 '''
        cls._client[client_name] = (conn, addr)
        cls._client_device[client_name] = {}

    def delClient(cls, client_name):
        '''TCP 접근 유저 삭제 '''
        del cls._client[client_name]
        del cls._client_device[client_name]

    def remove(cls):
        ''' 인스턴스 제거  '''
        cls = None