import json
import requests
import sys
import time


sys.path.append('/Users/zhuzhanhao/Testapi')

from Api.webuitest.conn_database import ConnDataBase


url="http://amberdata.cn/adminapi/v2/user/login"

con = ConnDataBase()
sysadmin = con.get_logininfo("sysadmin")
admin = con.get_logininfo("admin")
ast = con.get_logininfo("ast")



class GetToken:
    def __init__(self):
        self.con = ConnDataBase()
        self.yjadmin = self.con.get_logininfo("yjadmin")
        self.sysadmin = self.con.get_logininfo("sysadmin")
        self.admin = self.con.get_logininfo("admin")
        self.ast = self.con.get_logininfo("ast")


    def get_token_by_role(self,role):
        headers = {
            "Content-Type": "application/json"
        }
        #ERMS档案员
        if role == "ast":
            params = {
                "loginName": self.ast[0],
                "password": self.ast[1]
            }
        # ERMS单位管理员
        elif role == "admin":
            params = {
                "loginName": self.admin[0],
                "password": self.admin[1]
            }
        # ERMS系统管理员
        elif role == "sysadmin":
            params = {
                "loginName": self.sysadmin[0],
                "password": self.sysadmin[1]
            }
        #Transfer管理员
        elif role == "yjadmin":
            params = {
                "loginName": self.yjadmin[0],
                "password": self.yjadmin[1]
            }
        response = requests.post(url, headers=headers, data=json.dumps(params))
        res = response.json()['accessToken']
        # print(res)
        result = self.con.update_token(res, role)
        return result  # None


if __name__ == "__main__":
    start_time = time.time()
    a = GetToken()
    # print(a.get_json(a.get_user_power("ast")))
    print(a.get_token_by_role("ast"))
    end_time = time.time()
    print(round(end_time-start_time,3))

