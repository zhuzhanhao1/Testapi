import json

a = '''{
  "查询单位信息": {
    "data": null,
    "error": "Bad Request",
    "message": "请求的单位未找到",
    "path": "http://localhost:8080/ermsapi/unit/get_unit_by_group_name",
    "status": 400,
    "timestamp": 1567863429002
  },
  "查询单位信息运行时间为": "1.34秒",
  "＜1＞负责人": ""
}
'''
b = json.loads(a)
print(b)
print(type(b))
c = b["查询单位信息"]["message"]

print(type(c))
# del c["data"]
# del c["error"]
print(c)

