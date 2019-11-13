import os
import json
import requests

currentUrl = os.path.dirname(__file__)
print(currentUrl)
path = "/Users/zhuzhanhao/Desktop/zzh"

folder = path + "/Testoriginaldata"
if not os.path.exists(folder):
    os.mkdir(folder)

a = 1
for i in range(10):
    filename = "A001-WS-2019-{}".format(a) + ".xlsx"
    f = open(folder+"/"+filename,"w")
    f.write("This is {} time".format(a))
    f.close()
    a += 1
