#!/usr/bin/env python3
#-*- encoding: utf-8 -*-
import psutil
import math
import datetime
import pythoncom
import win32com.client
import asyncio

class Device:
    '''
    클라이언트 정보(윈도우) 추출 함수
    author: 이재영 (Jae Young Lee)
    '''
    def job_sys_status(self):
        # 리턴 Dic
        sys_status = {
            "data": {
                "store": [],
                "service": [],
                "taskscheduler":[]
            }
        }

        # 클라이언트 파티션 용량 체크
        for disk in psutil.disk_partitions():
            sys_store_status = {
                "name": None,
                "total": None,
                "used": None,
                "free": None,
                "percent": None
            }

            if disk.fstype:
                if str(disk.device)[0:1] :
                    sys_store_status["name"] = str(disk.device)[0:1]
                    sys_store_status["total"] = math.trunc(psutil.disk_usage(disk.mountpoint).total/1024/1024/1024*100)/100
                    sys_store_status["used"] = math.trunc(psutil.disk_usage(disk.mountpoint).used/1024/1024/1024*100)/100
                    sys_store_status["free"] = math.trunc(psutil.disk_usage(disk.mountpoint).free/1024/1024/1024*100)/100
                    sys_store_status["percent"] = math.trunc(psutil.disk_usage(disk.mountpoint).percent*100)/100
                sys_status['data']['store'].append(sys_store_status);

        # 클라이언트 서비스 명 체크
        for service in psutil.win_service_iter():
            sys_service_status = {}
            sys_service_status["name"] = service.display_name()
            sys_service_status["desc"] = service.description()
            sys_service_status["status"] = service.status()
            sys_service_status["startType"] = service.start_type()
            sys_service_status["logon"] = service.username()
            sys_status['data']['service'].append(sys_service_status)

        # 클라이언트 작업스케줄러 체크
        sys_status["data"]['worked'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        TASK_STATE = {0: 'Unknown',
                      1: '사용 안함',
                      2: '대기',
                      3: '준비',
                      4: '시작'}

        pythoncom.CoInitialize()
        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()
        folders = [scheduler.GetFolder('\\')]

        while folders:
            folder = folders.pop(0)
            folders += list(folder.GetFolders(0))
            for task in folder.GetTasks(0):
                sys_service_task = {
                    "name": None,
                    "path": None,
                    "status": None,
                    "lastRunTime": None,
                    "lastResult": None
                }
                path = task.Path.split("\\")
                sys_service_task["name"] = path[len(path)-1]
                del path[len(path)-1]
                fullpath = ""
                for p in path :
                    fullpath = fullpath + "\\" + p

                    sys_service_task["path"] = fullpath
                    sys_service_task["status"] = TASK_STATE[task.State]
                    sys_service_task["lastRunTime"] = str(task.LastRunTime)
                    lastTaskResult = str(hex(task.LastTaskResult))

                    # int 범위 오버플로우 값 맞춤
                    if task.LastTaskResult < 0:
                        if lastTaskResult == "-0x7ffb11fc":
                            lastTaskResult = "0x8004EE04"
                        elif lastTaskResult == "-0x7ff8ef20":
                            lastTaskResult = "0x800710E0"
                        elif lastTaskResult == "-0x7fffffe6":
                            lastTaskResult = "0x8000001A"
                        elif lastTaskResult == "-0x7ff8fbd5":
                            lastTaskResult = "0x80070428"
                    sys_service_task["lastResult"] = lastTaskResult
                sys_status['data']['taskscheduler'].append(sys_service_task)

        for a in sys_status['data']['taskscheduler']:
            print(a)

        pythoncom.CoUninitialize()
        return sys_status