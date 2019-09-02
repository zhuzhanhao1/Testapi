#单位档案员登录
def ast_login():
    params = {
        "loginName":ast[0],
        "password":ast[1]
    }
    headers = {
        "Content-Type":"application/json"
    }
    response = requests.post(url,headers=headers,data=json.dumps(params))
    return response.json()['accessToken']

#系统管理员登录
def sysadmin_login():
    params = {
        "loginName":sysadmin[0],
        "password":sysadmin[1]
    }
    headers = {
        "Content-Type":"application/json"
    }
    response = requests.post(url,headers=headers,data=json.dumps(params))
    return response.json()['accessToken']

#单位管理员登录
def admin_login():
    params = {
        "loginName":admin[0],
        "password":admin[1]
    }
    headers = {
        "Content-Type":"application/json"
    }
    response = requests.post(url,headers=headers,data=json.dumps(params))
    return response.json()['accessToken']

class ReqParam:
    #获取请求头数据
    def get_user_power(self,val):
        headers = None
        if val == "ast":
            print("当前用户:<{}>".format(ast[0]))
            headers = {"accessToken": ast_login()}
        elif val == "admin":
            print("当前用户:<{}>".format(admin[0]))
            headers = {"accessToken": admin_login()}
        else:
            print("当前用户:<{}>".format(sysadmin[0]))
            headers = {"accessToken": sysadmin_login()}
        return headers

    def get_json(self,val):
        json_str = json.dumps(val, ensure_ascii=False, sort_keys=True, indent=2)
        return json_str