import sys,os,time,datetime
import threading
import requests
import json

sys.path.append('/Users/zhuzhanhao/Testapi')

# currentUrl = os.path.dirname(__file__)
# cur_path = os.path.abspath(os.path.join(currentUrl,os.pardir))
# sys.path.append(cur_path)

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
                "parentId": "/安铂数据/文件整理/1996/KJ.科技档案/B.科技案件",
                "collectionWay":"record",
                "aclName":None,
                "metadataSchemeId": "7f18e50f-c57d-4285-9951-6c4c38e88837"
            }
            data={
              "record": {
                "version_no": "6",
                "metadata_scheme_id": "7f18e50f-c57d-4285-9951-6c4c38e88837",
                "metadata_scheme_name": "科技案件",
                "property": [
                  {
                    "name": "da_title",
                    "title": "题名",
                    "content": "测试{}".format(i)
                  },
                  {
                    "name": "da_archival_id",
                    "title": "档号/件号",
                    "content": ""
                  },
                  {
                    "name": "da_secrets_class",
                    "title": "密级",
                    "content": "MM"
                  },
                  {
                    "name": "da_opening_class",
                    "title": "开放等级",
                    "content": "01"
                  },
                  {
                    "name": "da_retention_period",
                    "title": "保管期限",
                    "content": "C"
                  }
                ],
                "block": [
                  {
                    "name": "基本信息",
                    "property": [
                      {
                        "name": "DAGMC",
                        "title": "档案馆名称",
                        "content": ""
                      },
                      {
                        "name": "DAGDM",
                        "title": "档案馆代码",
                        "content": ""
                      },
                      {
                        "name": "da_fonds_id",
                        "title": "全宗号",
                        "content": "J001"
                      },
                      {
                        "name": "da_filed_by",
                        "title": "归档者",
                        "content": "朱占豪"
                      },
                      {
                        "name": "da_transfer_by",
                        "title": "移交人",
                        "content": ""
                      },
                      {
                        "name": "da_transfer_date",
                        "title": "移交时间",
                        "content": ""
                      },
                      {
                        "name": "da_identity_by",
                        "title": "鉴定人",
                        "content": "朱占豪"
                      },
                      {
                        "name": "da_file_year",
                        "title": "年度",
                        "content": "1996"
                      },
                      {
                        "name": "da_sort_number",
                        "title": "排序号",
                        "content": ""
                      },
                      {
                        "name": "da_classification",
                        "title": "分类号",
                        "content": ""
                      },
                      {
                        "name": "da_is_classified",
                        "title": "是否已经分类",
                        "content": ""
                      },
                      {
                        "name": "da_identity_date",
                        "title": "鉴定时间",
                        "content": ""
                      },
                      {
                        "name": "da_record_authors",
                        "title": "责任者",
                        "content": ""
                      },
                      {
                        "name": "da_eventoccureddate",
                        "title": "事件发生时间",
                        "content": ""
                      },
                      {
                        "name": "da_page_number",
                        "title": "页号",
                        "content": ""
                      },
                      {
                        "name": "da_document_number",
                        "title": "文件编号",
                        "content": ""
                      },
                      {
                        "name": "da_pages",
                        "title": "页数",
                        "content": ""
                      },
                      {
                        "name": "da_filed_date",
                        "title": "归档时间",
                        "content": "2019-08-14T16:00:00.000Z"
                      }
                    ]
                  },
                  {
                    "file": {
                      "size": "",
                      "name": "",
                      "type": "电子文件",
                      "url": "",
                      "md5": ""
                    },
                    "name": "电子文件"
                  }
                ],
                "create_date": "2019-08-15",
                "modify_date": "2019-08-15",
                "template_id": "4dd9501c-6aa7-405c-8418-78e80c271b81",
                "name": "科技案件",
                "id": "7f18e50f-c57d-4285-9951-6c4c38e88837"
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
    L = {58:101}
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













