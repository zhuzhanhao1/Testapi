import sys,os,time,datetime
import threading
import requests
import json

sys.path.append('/Users/zhuzhanhao/Testapi')

# currentUrl = os.path.dirname(__file__)
# cur_path = os.path.abspath(os.path.join(currentUrl,os.pardir))
# sys.path.append(cur_path)
from Api.webuitest.conn_database import ConnDataBase
from Api.interfacetest.get_header import ReqParam

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
            data={
              "record": {
                "version_no": "1",
                "metadata_scheme_id": "e32753ff-4b6b-4f3f-8513-bfc9adab2deb",
                "metadata_scheme_name": "文书案件",
                "property": [
                  {
                    "name": "fonds_id",
                    "title": "全宗号",
                    "content": "A001"
                  },
                  {
                    "name": "filed_by",
                    "title": "归档者",
                    "content": "朱占豪"
                  },
                  {
                    "name": "filed_date",
                    "title": "归档时间"
                  },
                  {
                    "name": "transfer_by",
                    "title": "移交人"
                  },
                  {
                    "name": "transfer_date",
                    "title": "移交时间"
                  },
                  {
                    "name": "title",
                    "title": "题名",
                    "content": "教育科研会第{}场".format(i)
                  },
                  {
                    "name": "archival_id",
                    "title": "档号/件号",
                    "content": ""
                  },
                  {
                    "name": "security_class",
                    "title": "密级",
                    "content": "MM"
                  },
                  {
                    "name": "open_class",
                    "title": "开放等级",
                    "content": "01"
                  },
                  {
                    "name": "retention_period",
                    "title": "保管期限",
                    "content": "C"
                  },
                  {
                    "name": "identity_by",
                    "title": "鉴定人"
                  },
                  {
                    "name": "file_year",
                    "title": "年度",
                    "content": "2019"
                  },
                  {
                    "name": "classification",
                    "title": "分类号"
                  },
                  {
                    "name": "whether_classified",
                    "title": "是否已经分类"
                  },
                  {
                    "name": "identity_date",
                    "title": "鉴定时间"
                  },
                  {
                    "name": "record_authors",
                    "title": "责任者"
                  },
                  {
                    "name": "eventoccureddate",
                    "title": "事件发生时间"
                  },
                  {
                    "name": "page_number",
                    "title": "页号",
                    "content": "3"
                  },
                  {
                    "name": "document_number",
                    "title": "文件编号"
                  },
                  {
                    "name": "pages",
                    "title": "页数",
                    "content": "1"
                  }
                ],
                "block": {
                  "file": {
                    "size": "",
                    "name": "",
                    "type": "电子文件",
                    "url": "",
                    "md5": ""
                  },
                  "name": "电子文件"
                },
                "create_date": "2019-08-27",
                "modify_date": "2019-08-27",
                "template_id": "10e6ad95-71bb-43be-b1bf-8cd8c6c0045d",
                "name": "文书案件",
                "id": "e32753ff-4b6b-4f3f-8513-bfc9adab2deb"
              }
            }
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













