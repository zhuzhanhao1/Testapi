import sys, datetime
import threading
import requests
import json

import os
cur_path = os.path.dirname(os.path.realpath(__file__))
# print(cur_path)
cur_path1 = os.path.dirname(os.path.realpath(cur_path))
cur_path2 = os.path.dirname(os.path.realpath(cur_path1))
# print(cur_path2)
sys.path.append(cur_path2)
sys.path.append('/Users/zhuzhanhao/Testapi')

# currentUrl = os.path.dirname(__file__)
# cur_path = os.path.abspath(os.path.join(currentUrl,os.pardir))
# sys.path.append(cur_path)
from common.conn_database import ConnDataBase

q = 0
class ImportData:
    def __init__(self):
        self.con = ConnDataBase()
        token = self.con.get_logininfo("ast")[3]
        self.headers = {
            "accessToken": token
        }
        self.url = "http://amberdata.cn/ermsapi/v2/record/create_record"


    def import_data(self,start_user,end_user):
        global q
        for i in range(start_user, end_user):
            # print(i)
            self.headers["Content-Type"] = "application/json"
            params = {
                "actionType":1,
                "parentId": "/安铂数据/文件整理/2019/WS.文书档案/B.组织人事/4fc43b08-39f2-4a69-889e-2763242e86ad",
                "collectionWay":"volume",
                "aclName":None,
                "metadataSchemeId": "e32753ff-4b6b-4f3f-8513-bfc9adab2deb"
            }
            data={}
            res = requests.post(url=self.url,headers=self.headers,params=params,data=json.dumps(data))
            # print(res)
            if res.text == "true":
                q += 1
                print(q)
            else:
                print("出现异常，请查看日志")
                break


if __name__ == "__main__":
    L = {50:100,100:150,150:200,200:250}
    thread = []
    for start,end in L.items():
        t = threading.Thread(target=ImportData().import_data,args=(start,end))
        thread.append(t)

    start_time = datetime.datetime.now()
    for i in range(len(thread)):
        thread[i].start()

    for w in range(len(thread)):
        thread[w].join()
    end_time = datetime.datetime.now()

    run_time = end_time - start_time
    print(run_time)

    print("运行已结束")













