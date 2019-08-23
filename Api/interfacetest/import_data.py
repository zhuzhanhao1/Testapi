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
        self.url = "http://amberdata.cn/ermsapi/v2/volume/create_volume"


    def import_data(self,start_user,end_user):
        global q
        for i in range(start_user, end_user):
            # print(i)
            self.header["Content-Type"] = "application/json"
            params = {
                "actionType":0,
                "parentId": "/安铂数据/文件整理/2018/ZY.专业档案/A.专业案卷",
                "aclName":None,
                "metadataSchemeId": "f74a6f13-25e2-42b2-acc2-a239c79e7abe"
            }
            data={
              "record": {
                "version_no": "1",
                "metadata_scheme_id": "f74a6f13-25e2-42b2-acc2-a239c79e7abe",
                "metadata_scheme_name": "专业案卷",
                "property": [
                  {
                    "name": "fonds_id",
                    "title": "全宗号",
                    "content": "A001"
                  },
                  {
                    "name": "id",
                    "title": "案卷号",
                    "content": "{}".format(i)
                  },
                  {
                    "name": "identity_by",
                    "title": "鉴定人"
                  },
                  {
                    "name": "identity_date",
                    "title": "鉴定时间"
                  },
                  {
                    "name": "filed_by",
                    "title": "归档者"
                  },
                  {
                    "name": "filed_date",
                    "title": "归档时间"
                  },
                  {
                    "name": "retention_period",
                    "title": "保管期限",
                    "content": "C"
                  },
                  {
                    "name": "title",
                    "title": "案卷题名",
                    "content": "测试案卷{}".format(i)
                  },
                  {
                    "name": "transfer_by",
                    "title": "移交者"
                  },
                  {
                    "name": "transfer_date",
                    "title": "移交时间"
                  },
                  {
                    "name": "archival_id",
                    "title": "案卷档号",
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
                    "name": "sort_number",
                    "title": "排序号"
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
                    "name": "file_year",
                    "title": "年度",
                    "content": "2019"
                  },
                  {
                    "name": "file_start_date",
                    "title": "起始日期 -> 起始时间"
                  },
                  {
                    "name": "file_end_date",
                    "title": "终止日期 -> 终止时间"
                  },
                  {
                    "name": "pages",
                    "title": "页数"
                  }
                ],
                "create_date": "2019-08-20",
                "modify_date": "2019-08-20",
                "template_id": "df94a0f5-0351-4095-a452-e1b8ab4dca56",
                "name": "专业案卷",
                "id": "f74a6f13-25e2-42b2-acc2-a239c79e7abe"
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
    L = {2:11}
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













