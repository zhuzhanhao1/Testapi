import os
import json

# currentUrl = os.path.dirname(__file__)
# print(currentUrl)
# path = "/Users/zhuzhanhao/Desktop/zzh"
#
# folder = path + "/Testoriginaldata"
# if not os.path.exists(folder):
#     os.mkdir(folder)
#
# a = 1
# for i in range(10):
#     filename = "A001-WS-2019-{}".format(a) + ".xlsx"
#     f = open(folder+"/"+filename,"w")
#     f.write("This is {} time".format(a))
#     f.close()
#     a += 1

# a = '[{"prefix":"and","field":"casename","mode":"condition","type":"eq","value":"创建","id":1}]'
# f = json.loads(a)[0].get("value")
# print(type(json.loads(a)[0]))
# print(f)
# b = list(a)
# d = a.split(",")
# for i in d:
#     print(i)
#     e = i[4]
#
# print(e)
# c = ",".join(b)
# print(d)
a = "{\n  \"A.响应时长\": \"0.528秒\",\n  \"归档\": {\n    \"data\": null,\n    \"error\": \"Bad Request\",\n    \"message\": \"empty String\",\n    \"path\": \"http://localhost:8080/ermsapi/archives/file\",\n    \"status\": 400,\n    \"timestamp\": 1569556784063\n  }\n}"
b = json.loads(a)
d = [b]
c = json.dumps(b)
print(d)