#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
import json
import time, datetime
import socket
import asyncio
from common.thread.threadDev import ThreadDev

#TCP 클라이언트 공통 모듈
class TCPClient:
    _instance = None
    _sock = None
    _host = None
    _port = None

    def __new__(cls, host=None, port=None):
        if not cls._instance:
            cls._host = host
            cls._port = port
            cls._instance = object.__new__(cls)
        return cls._instance

    # TCP 서버 실행
    def runBatch(cls, workFunction):
        cls._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls._sock.connect((cls._host, cls._port))
        if (cls._sock):
            threadDev = ThreadDev()
            print("Command 서버 연결됨 ")
            threadDev.run('check', cls.rcvChk, ())
            cls.rcvMsg(workFunction)

    # TCP 서버에 메시지 전송
    def reMsg(cls, msg):
        result = {"result":True}
        try:
            cls._sock.send(msg.encode())
        except Exception as ex:
            result = { "result":False, "msg":ex }
            print(result);
        return result

    # TCP 서버 연결 체크
    def rcvChk(cls):
        while True:
            checkTime = datetime.datetime.now()
            time.sleep(120)
            result = cls.reMsg('{"check":1}')
            print(f"{checkTime} - 서버 접속 체크-{result}")
            if not result["result"]:
                break;

    # TCP 서버 명령 대기
    def rcvMsg(cls, workFunction):
        while True:
            try:
                data = cls._sock.recv(1024)
                now = datetime.datetime.now()
                if not data:
                    continue
                print(str(now)+":"+data.decode())
                msg = json.loads(data.decode())
                asyncio.run(workFunction(None, msg['job']))

            except Exception as ex:
                print(str(ex))
                if str(ex).find("[WinError 10054]") == 0:  # 서버 접근이 끊길 경우
                    msg = str(ex)
                    return msg
                elif str(ex).find("[WinError 10038]") == 0:  # 서버 접근이 끊길 경우
                    msg = str(ex)
                    return msg
                elif str(ex).find("[WinError 10053 ]") == 0:  # 서버 접근이 끊길 경우
                    msg = str(ex)
                    return msg
                else:
                    time.sleep(1000)
