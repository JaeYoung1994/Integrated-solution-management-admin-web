#!/usr/bin/env python3
#-*- encoding: utf-8 -*-
import time
import asyncio

from common.socket.tcp.client.tcpClient import TCPClient
from common.thread.threadDev import ThreadDev

from app.device.device import Device
from common.utils import Utils
from common.init import Init

HOST = 'shiptroll.com'
PORT = 20000
HOST = '192.168.219.102'
PORT = 9009

async def worker(cate, msg):
    tcpClient = TCPClient()
    if msg == 'init':
        time.sleep(1)
        ip = Utils.ipCheck()
        reMsg = ip
        tcpClient.reMsg(reMsg)
    if msg == 'sync_system_status':
        device = Device()
        result = device.job_sys_status()
        ip = Utils.ipCheck()
        result["ip"] = ip
        url = Init.getCommandPath() + "/save/client/device/info"
        req = Utils.requestUrl(method='POST', url=url, json=result)

'''
===================================
:mod:`main` 모듈 
===================================
관련 작업자
===========
* 이재영 (Lee, Jae Young)<shiptroll@gmail.com>
작업일지
--------
 *2016.04.19 Kei : 검사 엔진이 구현해야 할 함수 정의
'''
if __name__ == "__main__":
    # thread 공통 함수
    threadDev = ThreadDev()
    tcpClient = TCPClient(host=HOST, port=PORT)
    while True:
        # thread 실행 여부 체크
        if not threadDev.state('tcpClient')["result"]:
            threadDev.run("tcpClient", tcpClient.runBatch, (worker,))
        time.sleep(30);