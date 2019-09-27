import requests,json
import sys,os
cur_path = os.path.dirname(os.path.realpath(__file__))
cur_path1 = os.path.dirname(os.path.realpath(cur_path))
sys.path.append(cur_path1)

from Api.webuitest.conn_database import ConnDataBase


class RequestMethod():
    def __init__(self,val):
        self.val = val
        self.con = ConnDataBase()


    def get(self,url,params):
        token = self.con.get_logininfo(self.val)[3]
        headers = {
            "accessToken": token
        }
        r = requests.get(url, params=params, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("GET请求出错",e)
            return r.text



    def post(self,url,params,data=None):
        data = json.dumps(data)
        token = self.con.get_logininfo(self.val)[3]
        headers = {
            "accessToken": token,
            "Content-Type": "application/json"
        }
        r = requests.post(url, params=params, data=data, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("POST请求出错", e)
            print("zzh测试啊"+r.text)
            print(type(r.text))
            return r.text


    def delfiles(self,url,data=None):
        data = json.dumps(data)
        token = self.con.get_logininfo(self.val)[3]
        headers = {
            "accessToken": token,
            "Content-Type": "application/json"
        }
        r = requests.delete(url, data=data, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("POST请求出错", e)
            return r.text

    def delfile(self,url,params):
        try:
            token = self.con.get_logininfo(self.val)[3]
            headers = {
                "accessToken":token
            }
            r =requests.delete(url,params=params,headers=headers)
            json_response = r.json()
            return json_response
        except Exception as e:
            print("DELETE请求出错",e)

    def putfile(self,url,params,data=None):
        data = json.dumps(data)
        token = self.con.get_logininfo(self.val)[3]
        headers = {
            "accessToken": token,
            "Content-Type": "application/json"
        }
        r = requests.put(url, params=params, data=data, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("PUT请求出错",e)
            return r.text

    def uploadfile(self,url,params,data):
        print(data['path'])
        print(type(data['path']))
        print(params)
        print(type(params))
        try:
            token = self.con.get_logininfo(self.val)[3]
            headers = {
                "accessToken":token
            }
            files = {"file":open(data['path'],"rb")}
            r =requests.post(url,params=params,files=files,headers=headers)
            print(r.text)
            json_response = r.json()
            return json_response
        except Exception as e:
            print("上传文件失败",e)



    def run_main(self,method,url,params,data=None):
        res = None
        if method == "get":
            res = self.get(url,params)

        elif method == 'post' and data == None:
            res = self.post(url,params)
        elif method == "post" and data != None:
            res = self.post(url,params,data)

        elif method == 'delete':
            res = self.delfile(url, params)
        elif method == "Delete":
            res = self.delfiles(url, data)

        elif method == 'put' and data == None:
            res = self.putfile(url, params)
        elif method == "put" and data != None:
            res = self.putfile(url, params, data)

        elif method == "file":
            res = self.uploadfile(url,params,data)

        return res




if __name__ == "__main__":
    a = RequestMethod("ast")
    aa = '{"pagingSort": {"currentPage": "1","pageSize": 50,"totalCount": 0,"sortField": None,"sortWay": None},"columns": []}'
    aa1 = eval(aa)
    params = '{"parentId":"/档案局new5/文件整理/1901/WS.文书档案/A.党群服务(按件)","isArrangeArea":"true"}'
    params = eval(params)
    bb = "post"
    cc = "http://demo.amberdata.cn/ermsapi/v2/navigation/get_object_list"
    b = a.run_main(bb,cc,params,aa1)

    print(b)