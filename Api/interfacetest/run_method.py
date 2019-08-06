import requests,json
import sys,os
cur_path = os.path.dirname(os.path.realpath(__file__))
cur_path1 = os.path.dirname(os.path.realpath(cur_path))
sys.path.append(cur_path1)
from .get_header import ReqParam

class RequestMethod():
    def __init__(self,val):
        self.val = val
        self.reqheader = ReqParam()


    def get(self,url,params):
        try:
            headers = self.reqheader.get_user_power(self.val)
            #print(headers)
            r = requests.get(url, params=params,headers=headers)
            json_response = r.json()
                # self.reqheader.get_json(r.json())
            return json_response
        except Exception as e:
            print("GET请求出错")



    def post(self,url,params,data=None):
        data = json.dumps(data)
        try:
            headers = self.reqheader.get_user_power(self.val)
            headers["Content-Type"] = "application/json"
            #print(headers)
            r =requests.post(url,params=params,data=data,headers=headers)
            json_response = r.json()
                # ReqParam().get_json(r.json())
            return json_response
        except Exception as e:
            print("POST请求出错")



    def delfile(self,url,params):
        try:
            headers = self.reqheader.get_user_power(self.val)
            r =requests.delete(url,params=params,headers=headers)
            json_response = r.json()
                # ReqParam().get_json(r.json())
            return json_response
        except Exception as e:
            print("DELETE请求出错")



    def putfile(self,url,params,data=None):
        data = json.dumps(data)
        try:
            headers = self.reqheader.get_user_power(self.val)
            print(headers)
            headers["Content-Type"] = "application/json"
            r =requests.put(url,params=params,data=data,headers=headers)
            json_response = r.json()
                # ReqParam().get_json(r.json())
            return json_response
        except Exception as e:
            print("PUT请求出错")



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

        elif method == 'put' and data == None:
            res = self.putfile(url, params)
        elif method == "put" and data != None:
            res = self.putfile(url, params, data)
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