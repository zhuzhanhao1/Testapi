import sys,os,time,datetime
import threading
import requests
import json

currentUrl = os.path.dirname(__file__)
cur_path = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(cur_path)

from Api.interfacetest.get_header import ReqParam

q = 0
class ImportData:
    def __init__(self):
        self.header = ReqParam().get_user_power("ast")
        self.url = "http://amberdata.cn/ermsapi/v2/record/create_record"


    def import_data(self,start_user,end_user):
        global q
        for i in range(start_user, end_user):
            # print(i)
            self.header["Content-Type"] = "application/json"
            params = {
                "actionType":1,
                "parentId": "/下城区红十字会/文件整理/2019/CS.测试档案/CSZY.测试专业案卷/9e3347a3-9a4d-45be-a94e-9085dd97cb47",
                "collectionWay":"volume",
                "aclName":None,
                "metadataSchemeId": "021e33ff-41fc-4339-b6f7-dceee06c61a6"
            }
            data= {
              "record": {
                "version_no": "3",
                "metadata_scheme_id": "021e33ff-41fc-4339-b6f7-dceee06c61a6",
                "metadata_scheme_name": "专业-案件",
                "property": [
                  {
                    "name": "da_fonds_id",
                    "title": "全宗号",
                    "content": "Z005"
                  },
                  {
                    "name": "da_identity_by",
                    "title": "鉴定人"
                  },
                  {
                    "name": "da_identity_date",
                    "title": "鉴定时间"
                  },
                  {
                    "name": "da_iled_by",
                    "title": "归档者"
                  },
                  {
                    "name": "da_filed_date",
                    "title": "归档时间"
                  },
                  {
                    "name": "da_retention_period",
                    "title": "保管期限",
                    "content": "C"
                  },
                  {
                    "name": "da_title",
                    "title": "题名",
                    "content": "测试卷内案件{}号".format(i)
                  },
                  {
                    "name": "da_transfer_by",
                    "title": "移交人"
                  },
                  {
                    "name": "da_transfer_date",
                    "title": "移交时间"
                  },
                  {
                    "name": "da_archival_id",
                    "title": "档号",
                    "content": ""
                  },
                  {
                    "name": "da_security_class",
                    "title": "密级",
                    "content": "MM"
                  },
                  {
                    "name": "da_open_class",
                    "title": "开放等级",
                    "content": "01"
                  },
                  {
                    "name": "da_sort_number",
                    "title": "排序号"
                  },
                  {
                    "name": "da_classification",
                    "title": "分类号"
                  },
                  {
                    "name": "da_is_classified",
                    "title": "是否已经分类"
                  },
                  {
                    "name": "da_file_year",
                    "title": "年度",
                    "content": "2019"
                  },
                  {
                    "name": "da_eventoccureddate",
                    "title": "事件发生时间"
                  },
                  {
                    "name": "da_pages",
                    "title": "页数"
                  },
                  {
                    "name": "da_page_number",
                    "title": "页号"
                  },
                  {
                    "name": "da_document_number",
                    "title": "文件编号"
                  },
                  {
                    "name": "da_record_authors",
                    "title": "责任者"
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
                "create_date": "2019-08-15",
                "modify_date": "2019-08-15",
                "template_id": "0b4579fa-96fd-4aae-beaf-984b57cc095b",
                "name": "专业-案件",
                "id": "021e33ff-41fc-4339-b6f7-dceee06c61a6"
              }
            }
            res = requests.post(url=self.url,headers=self.header,params=params,data=json.dumps(data))
            # print(res)
            if res.text == "true":
                q += 1
                print(q)
            else:
                print("出现异常，请查看日志")
                break


if __name__ == "__main__":
    L = {55:58}
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













