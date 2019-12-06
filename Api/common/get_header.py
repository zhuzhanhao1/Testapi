import json
import requests
import sys
import time
import os

cur_path = os.path.dirname(os.path.realpath(__file__))
# print(cur_path)
cur_path1 = os.path.dirname(os.path.realpath(cur_path))
cur_path2 = os.path.dirname(os.path.realpath(cur_path1))
# print(cur_path2)
sys.path.append(cur_path2)

# sys.path.append('/Users/zhuzhanhao/Testapi')

from common.conn_database import ConnDataBase


url="http://amberdata.cn/adminapi/user/login"

# logincon = ConnDataBase()
# sysadmin = con.get_logininfo("sysadmin")
# admin = con.get_logininfo("admin")
# ast = con.get_logininfo("ast")



class GetToken:
    def __init__(self,role):
        self.con = ConnDataBase()
        self.role = self.con.get_logininfo(role)

    def get_token_by_role(self,role):
        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "loginName": self.role[0],
            "password": self.role[1]
        }
        response = requests.post(url, headers=headers, data=json.dumps(params))
        res = response.json()['accessToken']
        print(res)
        result = self.con.update_token(res, role)
        print("角色" + role + "的Token已被更新")
        return result  # None


if __name__ == "__main__":
    start_time = time.time()
    a = GetToken("ast")
    # print(a.get_json(a.get_user_power("ast")))
    print(a.get_token_by_role("ast"))
    end_time = time.time()
    print(round(end_time-start_time,3))

