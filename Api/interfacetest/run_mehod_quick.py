import requests,json
import sys,os
cur_path = os.path.dirname(os.path.realpath(__file__))
cur_path1 = os.path.dirname(os.path.realpath(cur_path))
sys.path.append(cur_path1)



class RequestMethodQuick():
    def get(self,url,headers,params):
        params = json.loads(params)
        headers = json.loads(headers)
        params = params if any(params) == True else None
        headers = headers if any(headers) == True else None
        r = requests.get(url, params=params, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("GET请求出错",e)
            return r.text



    def post(self,url,headers,params,data):

        params = json.loads(params)
        headers = json.loads(headers)
        params = params if any(params) == True else None
        headers = headers if any(headers) == True else None
        if data:
            data = json.loads(data)
            data = data if any(data) == True else None
            r = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        else:
            r = requests.post(url, params=params, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("POST请求出错", e)
            return r.text


    def delete(self,url,headers,params,data):
        params = json.loads(params)
        headers = json.loads(headers)
        params = params if any(params) == True else None
        headers = headers if any(headers) == True else None
        if data:
            data = json.loads(data)
            data = data if any(data) == True else None
            r = requests.delete(url, params=params, data=json.dumps(data), headers=headers)
        else:
            r = requests.delete(url, params=params, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("POST请求出错", e)
            return r.text


    def put(self,url,headers,params,data):
        params = json.loads(params)
        headers = json.loads(headers)
        params = params if any(params) == True else None
        headers = headers if any(headers) == True else None
        if data:
            data = json.loads(data)
            data = data if any(data) == True else None
            r = requests.put(url, params=params, data=json.dumps(data), headers=headers)
        else:
            r = requests.put(url, params=params, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("PUT请求出错",e)
            return r.text


    def uploadfile(self,url,headers,params,data):
        params = json.loads(params)
        headers = json.loads(headers)
        params = params if any(params) == True else None
        headers = headers if any(headers) == True else None
        print(data['path'])
        print(type(data['path']))
        print(params)
        print(type(params))
        files = {"file": open(data['path'], "rb")}
        r = requests.post(url, params=params, files=files, headers=headers)
        try:
            json_response = r.json()
            return json_response
        except Exception as e:
            print("转换字典失败",e)
            print(r.text)
            return r.text



    def run_main(self,method,url,headers,params,data):
        res = None
        if method == "GET":
            res = self.get(url,headers,params)

        elif method == 'POST':
            res = self.post(url,headers,params,data)

        elif method == 'DELETE':
            res = self.delete(url, headers,params,data)

        elif method == 'PUT':
            res = self.put(url,headers, params,data)

        elif method == "FILE":
            res = self.uploadfile(url,headers,params,data)

        return res




if __name__ == "__main__":
    method = "PUT"
    url = 'http://amberdata.cn/transferapi/v2/transfer_form/update_transfer_form'
    headers = '{"Content-Type": "application/json", "accessToken": "90e83f1becfeddf8234a2690336c86e8"}'
    params = '{"id": "/档案移交/J010/2018/83ab27ef-8444-461d-a47d-08235fd9c2b1"}'
    data ='''{
        "record": {
            "version_no": "11",
            "metadata_scheme_id": "4773410f-4aef-4bbf-a9a0-10f1f0e9389d",
            "metadata_scheme_name": "移交表单",
            "property": [{
                "name": "work_name",
                "title": "交接工作内容",
                "content": "2018年科技案卷门类档案移交任务"
            }, {
                "name": "transfer_year",
                "title": "移交年度",
                "content": "2018"
            }, {
                "name": "category_name",
                "title": "移交门类",
                "content": "科技案卷"
            }, {
                "name": "description",
                "title": "内容描述",
                "content": ""
            }, {
                "name": "volume_amount",
                "title": "移交案卷数量",
                "content": "12"
            }, {
                "name": "record_amount",
                "title": "移交案件数量",
                "content": "20"
            }, {
                "name": "data_size",
                "title": "移交数据量",
                "content": "1.720744E7"
            }, {
                "name": "carrier_sort_number",
                "title": "载体起止顺序号"
            }, {
                "name": "carrier_types",
                "title": "载体类型规格",
                "content": "01"
            }, {
                "name": "transfer_fonds",
                "title": "移交全宗号",
                "content": "J010"
            }, {
                "name": "transfer_unit",
                "title": "移交单位名称",
                "content": "杭州市档案局"
            }, {
                "name": "accession_unit",
                "title": "接收单位名称",
                "content": "杭州市档案局"
            }, {
                "name": "transfer_preparer",
                "title": "移交填表人",
                "content": "陆慧"
            }, {
                "name": "transfer_preparer_date",
                "title": "移交填表时间",
                "content": "2019-09-29T16:02:28.827"
            }, {
                "name": "accession_preparer",
                "title": "接收填表人"
            }, {
                "name": "accession_preparer_date",
                "title": "接收填表时间"
            }, {
                "name": "transfer_reviewer",
                "title": "移交审核人",
                "content": ""
            }, {
                "name": "transfer_reviewer_date",
                "title": "移交审核时间",
                "content": ""
            }, {
                "name": "accession_reviewer",
                "title": "接收审核人"
            }, {
                "name": "accession_reviewer_date",
                "title": "接收审核时间"
            }, {
                "name": "transfer_unit_seal",
                "title": "移交印章图片"
            }, {
                "name": "transfer_unit_seal_date",
                "title": "移交印章时间"
            }, {
                "name": "accession_unit_seal",
                "title": "接收印章图片"
            }, {
                "name": "accession_unit_seal_date",
                "title": "接收印章时间"
            }, {
                "name": "accession_unit_accuracy",
                "title": "接收准确性校验"
            }, {
                "name": "accession_unit_integrity",
                "title": "接收完整性校验"
            }, {
                "name": "accession_unit_usability",
                "title": "接收可用性校验"
            }, {
                "name": "accession_unit_security",
                "title": "接收安全性校验"
            }, {
                "name": "transfer_unit_accuracy",
                "title": "移交准确性校验"
            }, {
                "name": "transfer_unit_integrity",
                "title": "移交完整性校验"
            }, {
                "name": "transfer_unit_usability",
                "title": "移交可用性校验"
            }, {
                "name": "transfer_unit_security",
                "title": "移交安全性校验"
            }, {
                "name": "transfer_unit_carrier",
                "title": "移交载体外观校验"
            }, {
                "name": "accession_unit_carrier",
                "title": "接收载体外观校验"
            }, {
                "name": "category_id",
                "title": "移交门类ID",
                "content": "9486801e-653d-488f-aad1-b492008f1059"
            }],
            "block": {
                "name": "节点0"
            }
        }
    }'''
    a = RequestMethodQuick()
    b = a.run_main(method,url=url,headers=headers,params=params,data=data)
