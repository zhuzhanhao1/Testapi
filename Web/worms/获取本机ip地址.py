# 可以封装成函数，方便 Python 的程序调用
import datetime
import socket
import time

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
"""
优雅的方式获取本机ip地址
"""

#
# def get_host_ip():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(('8.8.8.8', 80))
#         ip = s.getsockname()[0]
#     finally:
#         s.close()
#     return ip
#
#
# print(get_host_ip())
# tz = pytz.timezone('Asia/Shanghai')  # 东八区
# t = datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')[11:]


def get_webtask_times():
    a = time.time()
    a = round(a,0)
    print(a)
    #
    locals_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[11:]
    print(locals_time)
    locals_time_l = locals_time.split(":")
    print(locals_time_l)
    print(int(locals_time_l[0]))

    locals_time_sjc = int(locals_time_l[0]) * 60 * 60 + int(locals_time_l[1]) * 60 + int(locals_time_l[2])
    print(locals_time_sjc)
    # print(time.mktime(time.strptime(locals_time, "%a %b %d %H:%M:%S %Y")))
    #
    # t = (2019, 8, 27, 21, 38, 38, 1, 48, 0)
    # print(time.mktime(t))


get_webtask_times()