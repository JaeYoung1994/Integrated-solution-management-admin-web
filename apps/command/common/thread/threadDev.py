#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
import threading

class ThreadDev:
    _instance = None
    _job = {} # 프로세스 관리용 딕셔너리

    # 인스턴스 1회 생성
    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    # 프로세스 실행
    def run(cls, name, function, arg):
        if not cls._job.get(name):
            t = threading.Thread(target=function, args=arg)
            t.daemon = True
            cls._job[name] = t
            cls._job[name].start()

    # 작업 중인 프로세스 제거
    def alive(cls, name):
        if cls._job.get(name):
            return cls._job.get(name).is_alive()
        else:
            return False

    # 프로세스 목록 가져오기
    def getThread(cls):
        return cls._job
