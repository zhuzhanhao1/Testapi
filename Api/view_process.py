import os,sys
from datetime import datetime
import time
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import *
from Api.interfacetest.run_method import RequestMethod
from Api.interfacetest.get_header import ReqParam
from Api.webuitest.DingDing import send_ding

currentUrl = os.path.dirname(__file__)
#父文件路径
cur_path = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(cur_path)
from webuitest.conn_database import ConnDataBase


#接口api用例首页
def process_interface_view(request):
    id = request.session.get('id')
    uname = User.objects.get(id=id).uname
    a = request.GET.get("belong","")
    case_count = Processapi.objects.all().count()
    return render(request,"process_interface.html",{"user":uname,"abq":a,"case_count":case_count})


#用例列表
def processlist_view(request):
    casename = request.GET.get("key[casename]","")
    if casename:
        print("搜索的用例名是:"+casename)
    belong = request.GET.get('belong',"")
    print("请求进入的模块是:"+belong)
    if casename == "" and belong == "":
        apilists = Processapi.objects.filter()

    #流程接口
    elif belong == "unit":
        apilists = Processapi.objects.filter(belong="单位接口")
    elif belong == "policy":
        apilists = Processapi.objects.filter(belong="保留处置策略接口")
    elif belong == "data_form_config":
        apilists = Processapi.objects.filter(belong="数据表单配置接口")
    elif belong == "alc":
        apilists = Processapi.objects.filter(belong="访问控制策略接口")


    #按用例名称查询
    elif casename:
        apilists = Processapi.objects.filter(casename__contains=casename)
    L = []
    for weblist in apilists:
        data = {
            "caseid": weblist.caseid,
            "isprocess":weblist.isprocess,
            "identity": weblist.identity,
            "casename": weblist.casename,
            "url": weblist.url,
            "method": weblist.method,
            "params": weblist.params,
            "body": weblist.body,
            "result": weblist.result,
            "order_no":weblist.order_no,
            "depend_id":weblist.depend_id,
            "depend_key":weblist.depend_key,
            "replace_key":weblist.replace_key,
            "replace_position":weblist.replace_position,
        }
        L.append(data)
    print(len(L))
    print("此模块的用例个数为:"+str(len(L)))
    pageindex = request.GET.get('page', "")
    pagesize = request.GET.get("limit", "")
    pageInator = Paginator(L, pagesize)
    # 分页
    contacts = pageInator.page(pageindex)
    res = []
    for contact in contacts:
        res.append(contact)
    datas = {"code": 0, "msg": "用例列表展现", "count": len(L), "data": res}
    return JsonResponse(datas)



# 创建api用例
def create_processcase_views(request):
    if request.method == 'POST':
        casename = request.POST.get("casename", "")
        url = request.POST.get("url", "")
        method = request.POST.get("method", "")
        belong = request.POST.get("belong", "")
        params = request.POST.get("params", "")
        body = request.POST.get("body", "")
        identity = request.POST.get("identity", "")
        orderno = request.POST.get("orderno","")
        isprocess = request.POST.get("isprocess","")
        dependid = request.POST.get("dependid","")
        dependkey = request.POST.get("dependkey","")
        replacekey = request.POST.get("replacekey","")
        replaceposition = request.POST.get("replaceposition","")
        Processapi.objects.create(casename=casename, identity=identity, url=url,
                            method=method, params=params, body=body, belong=belong,
                            isprocess=isprocess,depend_id=dependid,depend_key=dependkey,
                            replace_key=replacekey,replace_position=replaceposition,order_no=orderno
                            )
        return HttpResponseRedirect("/ProcessIndex/")



#删除api用例
def delete_processcase_views(request):
    if request.method == "GET":
        ids = request.GET.get("ids","")
        if ids:
            print(ids)
            Processapi.objects.filter(caseid=ids).delete()
            return HttpResponse("删除成功")



#更新api用例
def update_processcase_views(request):
    if request.method == "GET":
        params = request.GET.get('params',"")
        body =request.GET.get("body","")
        ids = request.GET.get("ids","")
        print(ids)
        if params:
            print(params)
            if params == "null":
                Processapi.objects.filter(caseid=ids).update(params="")
            else:
                Processapi.objects.filter(caseid=ids).update(params=params)

        elif body:
            print(body)
            if body == "null":
                Processapi.objects.filter(caseid=ids).update(body="")
            else:
                Processapi.objects.filter(caseid=ids).update(body=body)
        return HttpResponse("编辑成功")



#更改用户信息
def update_userinfo_api_views(request):
    role = request.POST.get("identity","")
    username = request.POST.get("username","")
    password = request.POST.get("password","")
    if username:
        try:
            con = ConnDataBase()
            con.update_logininfo(username,password,role)
            return HttpResponseRedirect("/ProcessIndex/")
        except:
            print("修改用户信息失败")
            return HttpResponse("链接数据库失败、修改用户信息失败")

    else:
        return HttpResponse("必须输入用户名和用户密码！！！")


#执行用例
def run_processcase_views(request):
    con = ConnDataBase()
    URL = str(con.get_logininfo("sysadmin")[2], 'utf-8')
    ids= request.GET.get("caseid").split(",")[:-1]
    print(ids)
    if len(ids) == 1:
        print("单一接口测试")
        d = {}
        ucaseid = ids[0]
        id = Processapi.objects.get(caseid=ucaseid)
        identity = id.identity
        head = id.exceptres
        url = URL + id.url
        method = id.method
        params = id.params
        body = id.body
        casename = id.casename
        Runmethod = RequestMethod(identity)
        starttime = time.time()
        if body != "":
            body = eval(body)
            if params:
                params = eval(params)
            response = Runmethod.run_main(method, url, params, body)

        elif body == '':
            if params:
                params = eval(params)
            response = Runmethod.run_main(method, url, params, body)

        endtime = time.time()
        runtime = round(endtime - starttime,3)
        # 存为字典，转换为json格式
        d[casename] = response
        d[casename+"运行时间为"] = str(runtime)+"秒"
        d["＜"+ucaseid+"＞"+"负责人"] = head
        print(d)
        #json格式化
        djson = json.dumps(d, ensure_ascii=False,sort_keys=True, indent=2)
        if "<" in djson or ">" in djson:
            print('存在需要替换的符号')
            a = djson.replace("<","＜")
            print(a)
            b = a.replace(">","＞")
            print(b)
            Processapi.objects.filter(caseid=ucaseid).update(result=b)
        else:
            Processapi.objects.filter(caseid=ucaseid).update(result=djson)
        print(djson)
        #发送钉钉消息
        #send_ding(djson)
        return HttpResponse(djson)

    #多个接口测试的情况
    else:
        print("多个接口测试")
        #将每次运行的字典结果集用列表存储
        L = []
        for ucaseid in ids:
            #每次循环创建一个字典，存储每次运行结束的接口，KEY以用例名字，Value以响应结果
            d = {}
            id = Processapi.objects.get(caseid=ucaseid)
            identity = id.identity
            url = URL + id.url
            method = id.method
            params = id.params
            body = id.body
            casename = id.casename
            isprocess = id.isprocess
            depend_id = id.depend_id
            depend_key = id.depend_key
            replace_key = id.replace_key
            replace_position = id.replace_position
            head = id.exceptres
            Runmethod = RequestMethod(identity)

            #判断是否为流程测试接口，如果是的话先通过依赖数据的ID查询结果
            if isprocess == "True":
                print("我需要依赖别的接口哦！！！")
                dependid = Processapi.objects.get(caseid=depend_id)
                if "," in depend_key:
                    #存在多个key时需要拆分字符串，通过循环赋值给每个结果
                    transfer_key = depend_key.split(",")
                    print(transfer_key)
                    l = []
                    for key in transfer_key:
                        if key :
                            l.append(key)

                    need_key = replace_key.split(",")
                    print(need_key)

                    b = 0
                    for i in l:
                        #依赖的数据
                        depend_res = json.loads(dependid.result)[dependid.casename][0][i]
                        print(depend_res)
                        if replace_position == "body":
                            if type(body) == str:
                                body = eval(body)
                            body[(need_key[b])] = depend_res
                        elif replace_position == "params":
                            params = eval(params)
                            params[(need_key[b])] = depend_res
                        b += 1
                    print("更新后的:" + str(body))
                    print("更新后的:" + str(params))
                    if params:
                        if type(params) == str:
                            params = eval(params)
                    if body:
                        if type(body) == str:
                            body = eval(body)
                    starttime = time.time()
                    response = Runmethod.run_main(method, url, params, body)


                #处理保管期限的列表接口返回的值
                elif "/" in depend_key:
                    # 存在多个key时需要拆分字符串，通过循环赋值给每个结果
                    transfer_key = depend_key.split("/")
                    print(transfer_key)
                    need_key = replace_key.split("/")
                    print(need_key)

                    # 依赖的数据
                    depend_res = json.loads(dependid.result)[dependid.casename][(transfer_key[0])][0][(transfer_key[1])]
                    print(depend_res)
                    if replace_position == "body":
                        body = eval(body)
                        body[(need_key[0])] = depend_res
                    elif replace_position == "params":
                        params = eval(params)
                        params[(need_key[0])] = depend_res

                    print("更新后的:" + str(body))
                    print("更新后的:" + str(params))
                    if params:
                        if type(params) == str:
                            params = eval(params)
                    if body:
                        if type(body) == str:
                            body = eval(body)
                    starttime = time.time()
                    response = Runmethod.run_main(method, url, params, body)





            #不需要别的接口
            elif isprocess != "True":
                print("我不需要依赖别的接口！！！")
                #计算运行前的时间
                starttime = time.time()
                if body != "":
                    body = eval(body)
                    if params:
                        params = eval(params)
                    response = Runmethod.run_main(method, url, params, body)

                elif body == '':
                    if params:
                        params = eval(params)
                    response = Runmethod.run_main(method, url, params, body)
            endtime = time.time()
            runtime = round(endtime - starttime,3)
            print(runtime)

            d[casename] = response
            if runtime > 0.5 and runtime <= 1.0:
                d[casename+"运行时间为"] = str(runtime)+"秒"
            elif runtime > 3.0:
                d[casename +"运行时间为"] = str(runtime)+"秒"
            else:
                d[casename +"运行时间为"] = str(runtime)+"秒"
            d["＜"+ucaseid+"＞"+"负责人"] = head

            #将每个结果的字典存放在一个列表中
            L.append(d)
            # json格式化
            djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
            if "<" in djson or ">" in djson:
                print('存在需要替换的符号')
                a = djson.replace("<", "＜")
                print(a)
                b = a.replace(">", "＞")
                print(b)
                Processapi.objects.filter(caseid=ucaseid).update(result=b)
            else:
                #每次运行结束将每个接口返回的数据JOSN格式化存入数据库
                Processapi.objects.filter(caseid=ucaseid).update(result=djson)
            #print(L)
            #创建一个字典存储包含所有字典的列表
        dict = {}
        dict["流程接口响应结果"] = L
        #转换为JSON格式，且格式化
        djson_new = json.dumps(dict, ensure_ascii=False, sort_keys=True, indent=2)
        print(djson_new)
        # 发送钉钉消息
        #send_ding(djson_new)
        #将JSON数据返回给前端
        return HttpResponse(djson_new)
