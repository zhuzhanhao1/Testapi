import json
import requests
import os,sys



from Api.webuitest.conn_database import ConnDataBase




url="http://demo.amberdata.cn/ermsapi/v2/user/user_login"

ast = "wuyufei@amberdata.cn"
admin = "erwa@amberdata.cn"
sysadmin = "admin@amberdata.cn"
password = "Dctm@1234"


#单位档案员登录
def ast_login():
    params = {
        "loginName":ast,
        "password":password
    }

    response = requests.get(url,params=params)
    return response.json()['accessToken']

#系统管理员登录
def sysadmin_login():
    params = {
        "loginName":sysadmin,
        "password":password
    }
    response = requests.get(url,params=params)
    return response.json()['accessToken']

#单位管理员登录
def admin_login():
    params = {
        "loginName":admin,
        "password":password
    }
    response = requests.get(url,params=params)
    return response.json()['accessToken']

class ReqParam:
    #获取请求头数据
    def get_user_power(self,val):
        headers = None
        if val == "ast":
            print("当前用户:<{}>".format(ast))
            headers = {"accessToken": ast_login()}
        elif val == "admin":
            print("当前用户:<{}>".format(admin))
            headers = {"accessToken": admin_login()}
        else:
            print("当前用户:<{}>".format(sysadmin))
            headers = {"accessToken": sysadmin_login()}
        return headers

    def get_json(self,val):
        json_str = json.dumps(val, ensure_ascii=False, sort_keys=True, indent=2)
        return json_str


if __name__ == "__main__":
    # print(admin_login())
    # a = ReqParam()
    # print(a.get_user_power("ast"))
    con = ConnDataBase()
    print(con.get_logininfo("admin"))


