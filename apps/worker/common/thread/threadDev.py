#!/usr/local/bin/python3
#-*- encoding: utf-8 -*-
import threading

class ThreadDev:
    _instance = None
    _job = {} # 쓰레드 관리용 딕셔너리

    # 인스턴스 1회 생성
    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    # 쓰레드 실행
    def run(cls, name, function, arg):
        result = {"result": False}
        # 작업 목록에 존재하는지 여부 체크
        if cls._job.get(name):
            # 작업이 실행중인지 여부 체크
            if cls._job.get(name).is_alive():
                result['msg'] = 'f{name}은 실행 중입니다.'
                return result
            del cls._job[name]
        # 작업 실행
        t = threading.Thread(name=name, target=function, args=arg)
        t.daemon = True
        cls._job[name] = t
        cls._job[name].start()
        result['result'] = True
        return result

    # 쓰레드 실행 여부 확인
    def state(cls, name):
        result = { "result":False }
        # 작업 목록에 존재하는지 여부 확인
        if cls._job.get(name):
            # 작업이 동작중인지 확인
            if not cls._job.get(name).is_alive():
                del cls._job[name]
                result['msg'] = f"{name}의 작업은 실행하고 있지 않습니다."
            else:
                result['result'] = True
        else:
            result['msg'] = f"{name}의 작업은 실행하고 있지 않습니다."
        return result

    # 쓰레드 목록 가져오기
    def list(cls):
        return cls._job
