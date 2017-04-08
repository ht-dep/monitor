import asyncio
import websockets
import threading
import json
import random
# import cx_Oracle
# import pymysql
from agent_release import getMonitorData
data1 = [
    {
        "1": "Tiger Nixon",
        "2": "System Architect",
        "3": "$3,120",
        "4": "Tiger Nixon",
        "5": "System Architect",
        "6": "$3,120",
        "7": "System Architect",
        "8": "$3,120",
        "9": "System Architect",
        "10": "$3,120",
    },
]

data2 = [
    {
        "1": "Tiger Nixon",
        "2": "System Architect",
        "3": "$3,120",
        "4": "Tiger Nixon",
        "5": "System Architect",
        "6": "$3,120",
        "7": "System Architect",
        "8": "$3,120",
        "9": "System Architect",
        "10": "$3,120",

    },
    {
        "1": "Tiger Nixon",
        "2": "System Architect",
        "3": "$3,120",
        "4": "Tiger Nixon",
        "5": "System Architect",
        "6": "$3,120",
        "7": "System Architect",
        "8": "$3,120",
        "9": "System Architect",
        "10": "$3,120",

    },
]
data3 = [
    {
        "1": "Tiger Nixon",
        "2": "System Architect",
        "3": "$3,120",
        "4": "Tiger Nixon",
        "5": "System Architect",
        "6": "$3,120",
        "7": "System Architect",
        "8": "$3,120",
        "9": "System Architect",
        "10": "$3,120",

    },
    {
        "1": "Tiger Nixon",
        "2": "System Architect",
        "3": "$3,120",
        "4": "Tiger Nixon",
        "5": "System Architect",
        "6": "$3,120",
        "7": "System Architect",
        "8": "$3,120",
        "9": "System Architect",
        "10": "$3,120",

    },
    {
        "1": "Tiger Nixon",
        "2": "System Architect",
        "3": "$3,120",
        "4": "Tiger Nixon",
        "5": "System Architect",
        "6": "$3,120",
        "7": "System Architect",
        "8": "$3,120",
        "9": "System Architect",
        "10": "$3,120",

    },
    {
        "1": "Tiger Nixon",
        "2": "System Architect",
        "3": "$3,120",
        "4": "Tiger Nixon",
        "5": "System Architect",
        "6": "$3,120",
        "7": "System Architect",
        "8": "$3,120",
        "9": "System Architect",
        "10": "$3,120",

    },
]
data = [data1, data2,data3]

import time

data_json = []  # 定义全局变量

data_json=""
def send_data(data):
    # return json.dumps(getMonitorData)
    pass

#
# def check_key(json_data):
#     key = json.loads(json_data)
#     if key["key"] == "rinpo":
#         return True
#     return False


def handler_resultSet(result):
    per_card = {}
    if len(result):
        return []
    for i in result:
        # 未完成
        # per_card[""]=
        pass


# 数据查询线程
#暂时不用
# def run_flag():
#     global data_json
#     # conn = cx_Oracle.connect("wpms_user2", "oracle", "192.168.0.102:1521/RINPODB")
#     conn = pymysql.connect(host="127.0.0.1", user="root", password="131427", database="prj017", port=3306,
#                            charset='utf8')
#     h = conn.cursor()
#     print("开始查询数据库")
#     while 1:
#         with conn.cursor()as cursor:
#             sql = "select * from lib_admin_major"
#             cursor.execute(sql)
#             result = cursor.fetchall()
#
#         # 处理数据结构
#         result = handler_resultSet(result)
#         time.sleep(10)
#
def run_json_data():
    global data_json
    while 1:
        time.sleep(1)
        #是否组装列表
        # data_json=send_data(data)
        data_json=getMonitorData()
        # print(data_json)
        data.append()#列表添加五个，


async def hello(websocket, path):
    ccc = 1
    # recv_messgae = await websocket.recv()
    # flag = check_key(recv_messgae)
    while 1:
        print("循环次数：", ccc)
        # data_json=getMonitorData()
        # print("*****"+data_json)
        # data_json = send_data(data)
        await websocket.send(data_json)#发送数据
        await asyncio.sleep(5)
        print(">发送数据 {}".format(data_json))

        # print(recv_messgae)
        ccc += 1
        # print(ccc)


t1 = threading.Thread(target=run_json_data)
t1.start()
start_server = websockets.serve(hello, '0.0.0.0', 9999)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
