# 可以封装成函数，方便 Python 的程序调用
import datetime
import os
import socket
import time

import apscheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,date


import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

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


# def get_webtask_times():
#     a = time.time()
#     a = round(a,0)
#     print(a)
#     #
#     locals_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[11:]
#     print(locals_time)
#     locals_time_l = locals_time.split(":")
#     print(locals_time_l)
#     print(int(locals_time_l[0]))
#
#     locals_time_sjc = int(locals_time_l[0]) * 60 * 60 + int(locals_time_l[1]) * 60 + int(locals_time_l[2])
#     print(locals_time_sjc)
    # print(time.mktime(time.strptime(locals_time, "%a %b %d %H:%M:%S %Y")))
    #
    # t = (2019, 8, 27, 21, 38, 38, 1, 48, 0)
    # print(time.mktime(t))


# def job(a):
#     # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     # 获取本地当前时间 格式化格式
#     # locals_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))[11:]
#     locals_time = datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime(
#         '%Y-%m-%d %H:%M:%S')[11:]
#     locals_time_l = locals_time.split(":")
#     locals_time_sjc = int(locals_time_l[0]) * 60 * 60 + int(locals_time_l[1]) * 60 + int(locals_time_l[2])
#     print(locals_time_sjc)
#     if locals_time_sjc == 67210:
#         # print("aaaaaaaa")
#         print(a)
#
# def job_function(a):
#     print(a)
#
# # BlockingScheduler
# sched = BlockingScheduler()
# # # Schedule job_function to be called every two hours
# # # sched.add_job(job_function, 'interval', hours=2)
# # # The same as before, but starts on 2010-10-10 at 9:30 and stops on 2014-06-15 at 11:00
# a = "wwwwwww"
# job = sched.add_job(job_function, 'interval', seconds=5, start_date='2019-09-10 10:52:30', end_date='2019-09-10 22:55:30',args=(a,))
# sched.start()
#
#



# sched = BackgroundScheduler()
# def my_job():
#     print('Tick! The time is: %s' % datetime.now())
# # The job will be executed on November 6th, 2009
# # sched.add_job(my_job, 'date', run_date=date(2019, 9, 9), args=['text'])
# # sched.add_job(my_job, 'date', run_date=datetime(2019, 9, 9, 22, 38, 5), args=['text'])
# # sched.add_job(my_job, 'date', run_date='2019-09-09 22:38:05', args=['text'])
# # The 'date' trigger and datetime.now() as run_date are implicit
# sched.add_job(my_job, 'interval', seconds=3)
# print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
# sched.start()
# print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
# try:
#     # This is here to simulate application activity (which keeps the main thread alive).
#     while True:
#         time.sleep(2)    #其他任务是独立的线程执行
#         print('sleep!')
# except (KeyboardInterrupt, SystemExit):
#     # Not strictly necessary if daemonic mode is enabled but should be done if possible
#     sched.shutdown()start_date="2019-09-10 10:38:08", end_date="2019-09-10 10:39:08",
#     print('Exit The Job!')

def job_function(a):
    print(datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')[11:])
# BlockingScheduler
sched = BlockingScheduler()
a = "wwwwwwww"
job = sched.add_job(job_function,"interval",seconds = 5,args=(a,),start_date="2019-09-10 22:55:08", end_date="2019-09-10 23:55:08")
sched.start()

# print(sched.get_job(job_id='123'))BackgroundScheduler
print(sched.get_jobs())
# print(apscheduler)
# print(apscheduler.get_jobs())
# print(apscheduler.print_jobs())

print("我开始运行了")
# job.remove()
print("我被删除了")
# print(print_jobs())

# try:
#     sched.start()
#     print("我被阻塞了吗？")
#     # return HttpResponse("定时任务在后台已经开始")
# except(KeyboardInterrupt,SystemExit):
#     sched.shutdown()
#     print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

