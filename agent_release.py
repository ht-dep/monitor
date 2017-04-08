# _*_coding:utf-8_*_
__author__ = 'ht Qi'

import platform
import os
import psutil
import json
import socket
import time
import datetime


# 配置文件路径
def get_path():
    current_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_path, "config.json")
    return file_path


# 读取配置
def get_config():
    file_path = get_path()
    if os.path.exists(file_path):
        with open(file_path, encoding='utf8') as f:
            result = json.loads(f.read())
        return result


# 解析数据包
def unpack_data(data):
    data_dict = {}
    data_attrs_list = [i for i in dir(data) if not i.startswith('_')]
    for i in data_attrs_list:
        if i != 'index':
            if i != 'count':
                data_dict[i] = getattr(data, i)
    return data_dict


def getOS():
    content = platform.platform()
    # print("操作系统：{}".format(content))  # 需要 'OS'
    return content


# 'CLUSTER'
def getCpu():
    data = {"cores": {},
            "all_cpu_usage": {},
            "cpu_model": '',  # cpu的型号
            "cpu_num": int()  # cpu的虚拟核心数量
            }
    try:
        data['cpu_num'] = psutil.cpu_count()
        # 所有cpu的数据
        content = os.popen("wmic cpu get Name").read()
        list_content = [i for i in content.splitlines() if len(i) > 0]
        data["cpu_model"] = list_content[1]

        all_cpu = psutil.cpu_times()  # 应该加上  psutil.cpu_stats()
        data["all_cpu_usage"] = unpack_data(all_cpu)

        per_cpu = psutil.cpu_times(percpu=True)  # 每个逻辑cpu的数据列表
        i = 1
        for per in per_cpu:
            data["cores"]["core_" + str(i)] = unpack_data(per)
            i += 1
    except Exception as e:
        print("cpu_error:", e)
    return data


def getHostName():
    # HOSTNAME
    content = platform.node()
    return content


def getUptime():
    # 获取开机时间
    startUnixTime = psutil.boot_time()
    nowUnixTime = time.time()
    rangeUnixTime = nowUnixTime - startUnixTime
    online_time = time.strftime("%H:%M:%S", time.gmtime(rangeUnixTime))
    if rangeUnixTime > 24 * 60 * 60:
        a = str(int(rangeUnixTime / (24 * 60 * 60)))
        if len(a) < 2:
            online_time = "0" + a + " " + online_time
        else:
            online_time = a + " " + online_time

    print("开机时间：", online_time)
    return online_time


def getMemInfo():
    mem_dict = {}
    try:
        data = psutil.virtual_memory()

        mem_dict["mem_total"] = data.total
        mem_dict["mem_free"] = data.free

        swap_data = psutil.swap_memory()
        mem_dict["swap_free"] = swap_data.free
        mem_dict["swap_total"] = swap_data.total
    except Exception as  e:
        print("mem_error:", e)
    return mem_dict


def getLocalDiskPart():
    disk_part = {}
    try:
        content = psutil.disk_partitions()

        for part in content:
            disk_part[part.device] = {}
            if part.opts == "cdrom":
                disk_part[part.device] = "CD驱动器"
            else:
                disk_use = psutil.disk_usage(part.device)
                disk_part[part.device]["total"] = disk_use.total
                disk_part[part.device]["available"] = disk_use.free
                disk_part[part.device]["used"] = disk_use.used
                disk_part[part.device]["fs"] = part.fstype
    except Exception as e:
        print("disk_error:", e)
    return disk_part


def getNetworkInfo():
    NET = {
        "rx": {},
        "tx": {}
    }
    try:
        content = psutil.net_io_counters(pernic=True)
        list_key = content.keys()
        for i in list_key:
            NET["rx"][i] = content.get(i).bytes_recv
            NET["tx"][i] = content.get(i).bytes_sent
    except Exception as e:
        print("net_error:", e)

    return NET


def getLoadInfo():
    """ Returns a list CPU Loads"""

    try:
        result = psutil.cpu_percent(0.3)
    except Exception as e:
        print("error:", e)
        result = ''

    return result


def monitor(clusterName="win_PC"):
    data = {"OS": '',  # 系统版本
            "CLUSTER": '',  # 客户
            "HOSTNAME": '',  # 系统用户名
            "CPU": {},  # cpu详情
            "NET": {},  # 网卡
            "LOCALDISKPART": {},  # 磁盘
            "MEM": {},  # 内存
            "LOAD": {},  # 负载
            "UPTIME": {}  # 上线时间
            }

    data["OS"] = getOS()
    data["CLUSTER"] = clusterName
    data["HOSTNAME"] = getHostName()
    data["CPU"] = getCpu()
    data["NET"] = getNetworkInfo()
    data["LOCALDISKPART"] = getLocalDiskPart()  # capacity不知道是什么
    data["MEM"] = getMemInfo()
    data["LOAD"] = getLoadInfo()
    data["UPTIME"] = getUptime()

    json_data = json.dumps(data, ensure_ascii=False)
    return json_data


def sendData(data, serverIP, serverPort):
    ip = serverIP
    port = int(serverPort)
    addr = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    s.sendall(data)  # ht 2016.11.26
    s.close()  # ht

def getMonitorData():
    # jsonString = monitor(nodeName)
    jsonString = monitor("服务器监控1")
    print(jsonString)

    print("数据包长度：{}，当前时间：{}".format(len(jsonString), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    return jsonString
if __name__ == "__main__":
    getMonitorData()
    # agentCfg = get_config()
    # if agentCfg is None:
    #     print("配置文件'{}'不存在".format("config.json"))
    #     time.sleep(10)
    #
    # else:
    #     nodeName = agentCfg["name"]
    #     nodeIp = agentCfg["ip"]
    #     nodePort = agentCfg["port"]
    #     while True:
    #
    #         jsonString = monitor(nodeName)
    #         print(jsonString)
    #
    #         print("数据包长度：{}，当前时间：{}".format(len(jsonString), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    #
    #         try:
    #             sendData(jsonString.encode(), nodeIp, nodePort)
    #             # time.sleep(5)
    #         except:
    #             print("发送异常")
    #             pass
    #         time.sleep(5)