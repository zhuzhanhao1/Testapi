import os, sys, io
import threading

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import time
import json
import jsonpath
from apscheduler.triggers.interval import IntervalTrigger
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from xlwt import Workbook
from .forms import *
from Api.interfacetest.run_method import RequestMethod
import pytz
from Api.interfacetest.get_header import GetToken
from Api.webuitest.DingDing import send_ding,send_image,send_link

currentUrl = os.path.dirname(__file__)
# 父文件路径
cur_path = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(cur_path)
from webuitest.conn_database import ConnDataBase

num_progress = 0 # 全局变量进度数
thread_dict = {}


#流程测试接口列表
@login_required
def processlist_view(request):
    casename = request.GET.get("key[casename]", "")
    filterSos = request.GET.get("filterSos", "")
    belong = request.GET.get('belong', "")
    print("请求进入的模块是:" + belong)

    if casename == "" and belong == "" and filterSos== "":
        apilists = Processapi.objects.filter().order_by("sortid")

    # 流程接口
    if belong:
        if belong == "login":
            apilists = Processapi.objects.filter(belong="登录过程接口").order_by("sortid")
        elif belong == "policy":
            apilists = Processapi.objects.filter(belong="保留处置策略接口").order_by("sortid")
        elif belong == "data_form_config":
            apilists = Processapi.objects.filter(belong="数据表单配置接口").order_by("sortid")
        elif belong == "alc":
            apilists = Processapi.objects.filter(belong="访问控制策略接口").order_by("sortid")
        elif belong == "category":
            apilists = Processapi.objects.filter(belong="类目保管期限接口").order_by("sortid")
        elif belong == "view":
            apilists = Processapi.objects.filter(belong="视图自定义接口").order_by("sortid")
        elif belong == "finish_task":
            apilists = Processapi.objects.filter(belong="整理任务接口").order_by("sortid")

    # 按用例名称查询
    elif casename:
        print("搜索的用例名是:" + casename)
        apilists = Processapi.objects.filter(casename__contains=casename)
        print(apilists)
        # if apilists.count() == 0:
        if casename == "错误接口查询":
            apilists = Processapi.objects.filter().order_by("sortid")
            L = []
            for weblist in apilists:
                if weblist.system == "erms" and "error" in weblist.result and "timestamp" in weblist.result:
                    # print("存在的啊")
                    data = {
                        "caseid": weblist.caseid,
                        "isprocess": weblist.isprocess,
                        "identity": weblist.identity,
                        "casename": weblist.casename,
                        "url": weblist.url,
                        "method": weblist.method,
                        "params": weblist.params,
                        "body": weblist.body,
                        "result": weblist.result,
                        "sortid": weblist.sortid,
                        "depend_id": weblist.depend_id,
                        "depend_key": weblist.depend_key,
                        "replace_key": weblist.replace_key,
                        "replace_position": weblist.replace_position,
                        "belong": weblist.belong,
                        "head":weblist.header,
                        "duration": weblist.duration
                    }
                    L.append(data)
            print("此模块的用例个数为:" + str(len(L)))
            pageindex = request.GET.get('page', "")
            pagesize = request.GET.get("limit", "")
            pageInator = Paginator(L, pagesize)
            # 分页
            contacts = pageInator.page(pageindex)
            res = []
            for contact in contacts:
                res.append(contact)
            datas = {"code": 0, "msg": "", "count": len(L), "data": res}
            return JsonResponse(datas)

        elif casename == "A":
            apilists = Processapi.objects.filter().order_by("duration")
            L = []
            for weblist in apilists:
                if weblist.system == "erms" and weblist.duration >= 1:
                    # print("存在的啊")
                    data = {
                        "caseid": weblist.caseid,
                        "isprocess": weblist.isprocess,
                        "identity": weblist.identity,
                        "casename": weblist.casename,
                        "url": weblist.url,
                        "method": weblist.method,
                        "params": weblist.params,
                        "body": weblist.body,
                        "result": weblist.result,
                        "sortid": weblist.sortid,
                        "depend_id": weblist.depend_id,
                        "depend_key": weblist.depend_key,
                        "replace_key": weblist.replace_key,
                        "replace_position": weblist.replace_position,
                        "belong": weblist.belong,
                        "head":weblist.header,
                        "duration":weblist.duration
                    }
                    L.append(data)
            print("此模块的用例个数为:" + str(len(L)))
            pageindex = request.GET.get('page', "")
            pagesize = request.GET.get("limit", "")
            pageInator = Paginator(L, pagesize)
            # 分页
            contacts = pageInator.page(pageindex)
            res = []
            for contact in contacts:
                res.append(contact)
            datas = {"code": 0, "msg": "", "count": len(L), "data": res}
            return JsonResponse(datas)

        elif casename == "B":
            apilists = Processapi.objects.filter().order_by("duration")
            L = []
            for weblist in apilists:
                if weblist.system == "erms" and weblist.duration >= 3:
                    # print("存在的啊")
                    data = {
                        "caseid": weblist.caseid,
                        "isprocess": weblist.isprocess,
                        "identity": weblist.identity,
                        "casename": weblist.casename,
                        "url": weblist.url,
                        "method": weblist.method,
                        "params": weblist.params,
                        "body": weblist.body,
                        "result": weblist.result,
                        "sortid": weblist.sortid,
                        "depend_id": weblist.depend_id,
                        "depend_key": weblist.depend_key,
                        "replace_key": weblist.replace_key,
                        "replace_position": weblist.replace_position,
                        "belong": weblist.belong,
                        "head":weblist.header,
                        "duration":weblist.duration
                    }
                    L.append(data)
            print("此模块的用例个数为:" + str(len(L)))
            pageindex = request.GET.get('page', "")
            pagesize = request.GET.get("limit", "")
            pageInator = Paginator(L, pagesize)
            # 分页
            contacts = pageInator.page(pageindex)
            res = []
            for contact in contacts:
                res.append(contact)
            datas = {"code": 0, "msg": "", "count": len(L), "data": res}
            return JsonResponse(datas)


    elif filterSos:
        print(filterSos)
        if filterSos == "[]":
            apilists = Processapi.objects.filter(system="erms").order_by("sortid")
        else:
            L = []
            for i in json.loads(filterSos):
                filterSos_res = i.get("value")
                print(filterSos_res)
                apilists = Processapi.objects.filter(Q(casename__contains=filterSos_res) & Q(system="erms")).order_by("sortid")
                for weblist in apilists:
                    data = {
                        "caseid": weblist.caseid,
                        "isprocess": weblist.isprocess,
                        "identity": weblist.identity,
                        "casename": weblist.casename,
                        "url": weblist.url,
                        "method": weblist.method,
                        "params": weblist.params,
                        "body": weblist.body,
                        "result": weblist.result,
                        "sortid": weblist.sortid,
                        "depend_id": weblist.depend_id,
                        "depend_key": weblist.depend_key,
                        "replace_key": weblist.replace_key,
                        "replace_position": weblist.replace_position,
                        "belong": weblist.belong,
                        "head": weblist.header,
                        "duration": weblist.duration
                    }
                    L.append(data)
            print(L)
            print("此模块的用例个数为:" + str(len(L)))
            pageindex = request.GET.get('page', "")
            pagesize = request.GET.get("limit", "")
            pageInator = Paginator(L, pagesize)
            # 分页
            contacts = pageInator.page(pageindex)
            res = []
            for contact in contacts:
                res.append(contact)
            datas = {"code": 0, "msg": "", "count": len(L), "data": res}
            return JsonResponse(datas)

    L = []
    for weblist in apilists:
        data = {
            "caseid": weblist.caseid,
            "isprocess": weblist.isprocess,
            "identity": weblist.identity,
            "casename": weblist.casename,
            "url": weblist.url,
            "method": weblist.method,
            "params": weblist.params,
            "body": weblist.body,
            "result": weblist.result,
            "sortid": weblist.sortid,
            "depend_id": weblist.depend_id,
            "depend_key": weblist.depend_key,
            "replace_key": weblist.replace_key,
            "replace_position": weblist.replace_position,
            "belong": weblist.belong,
            "head": weblist.header,
            "duration":weblist.duration
        }
        L.append(data)
    print(len(L))
    print("此模块的用例个数为:" + str(len(L)))
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

#流程结果列表
@login_required
def process_result_list_views(request):
    caseids = request.GET.get("caseids","")
    print(caseids)
    print(type(caseids))
    L = []
    for i in json.loads(caseids):
        apilists = Processapi.objects.filter(Q(caseid=i) & Q(system="erms")).order_by("sortid")
        for weblist in apilists:
            data = {
                "casename": weblist.casename,
                "result": weblist.result,
                "head": weblist.header
            }
            L.append(data)
    print(L)
    print("此模块的用例个数为:" + str(len(L)))
    pageindex = request.GET.get('page', "")
    pagesize = request.GET.get("limit", "")
    pageInator = Paginator(L, pagesize)
    # 分页
    contacts = pageInator.page(pageindex)
    res = []
    for contact in contacts:
        res.append(contact)
    datas = {"code": 0, "msg": "", "count": len(L), "data": res}
    return JsonResponse(datas)


# 创建api用例
@login_required
def create_processcase_views(request):
    if request.method == 'POST':
        casename = request.POST.get("casename", "")
        url = request.POST.get("url", "")
        method = request.POST.get("method", "")
        belong = request.POST.get("belong", "")
        params = request.POST.get("params", "")
        body = request.POST.get("body", "")
        identity = request.POST.get("identity", "")
        isprocess = request.POST.get("isprocess", "")
        dependid = request.POST.get("dependid", "")
        dependkey = request.POST.get("dependkey", "")
        replacekey = request.POST.get("replacekey", "")
        replaceposition = request.POST.get("replaceposition", "")
        system = request.POST.get("system","")

        all = Processapi.objects.filter(system=system)
        L = []
        for i in all:
            L.append(i.sortid)
        m = max(L) + 1


        if "<" in body or ">" in body:
            print('存在需要替换的符号')
            a = body.replace("<", "＜")
            print(a)
            b = a.replace(">", "＞")
            print(b)
            Processapi.objects.create(casename=casename, identity=identity, url=url,system=system,
                                      method=method, params=params, body=b, belong=belong,
                                      isprocess=isprocess, depend_id=dependid, depend_key=dependkey,
                                      replace_key=replacekey, replace_position=replaceposition, sortid=m
                                      )
        else:
            Processapi.objects.create(casename=casename, identity=identity, url=url,system=system,
                                      method=method, params=params, body=body, belong=belong,
                                      isprocess=isprocess, depend_id=dependid, depend_key=dependkey,
                                      replace_key=replacekey, replace_position=replaceposition, sortid=m
                                      )
        return HttpResponse("操作成功")
    else:
        return HttpResponse("请求方式不对")


# 删除api用例
@login_required
def delete_processcase_views(request):
    if request.method == "GET":
        ids = request.GET.get("ids","")
        id = request.GET.get("id", "")
        if ids:
            caseids = json.loads(ids)
            print(ids)
            for caseid in caseids:
                Processapi.objects.filter(caseid=caseid.get("caseid","")).delete()
            return HttpResponse("操作成功")
        elif id:
            Processapi.objects.filter(caseid=id).delete()
            return HttpResponse("操作成功")
        else:
            return HttpResponse("没有获取请求的ID")
    else:
        return HttpResponse("请求方式有误")



# 更新api用例
@login_required
def update_processcase_views(request):
    if request.method == "GET":
        print("单个修改")
        params = request.GET.get('params', "")
        body = request.GET.get("body", "")
        ids = request.GET.get("ids", "")
        head = request.GET.get("head","")
        depend_id = request.GET.get('depend_id', "")
        depend_key = request.GET.get("depend_key", "")
        replace_key = request.GET.get("replace_key", "")
        replace_position = request.GET.get("replace_position","")
        print(ids)
        if params:
            print(params)
            if params == "1":
                Processapi.objects.filter(caseid=ids).update(params="")
            else:
                Processapi.objects.filter(caseid=ids).update(params=params)

        elif body:
            if body == "1":
                Processapi.objects.filter(caseid=ids).update(body="")
            elif "<" in body or ">" in body:
                print('存在需要替换的符号')
                a = body.replace("<", "＜")
                print(a)
                b = a.replace(">", "＞")
                print(b)
                Processapi.objects.filter(caseid=ids).update(body=b)
            else:
                Processapi.objects.filter(caseid=ids).update(body=body)
        elif head:
            print(head)
            Processapi.objects.filter(caseid=ids).update(header=head)
        elif depend_id:
            Processapi.objects.filter(caseid=ids).update(depend_id=depend_id)
        elif depend_key:
            Processapi.objects.filter(caseid=ids).update(depend_key=depend_key)
        elif replace_key:
            Processapi.objects.filter(caseid=ids).update(replace_key=replace_key)
        elif replace_position:
            Processapi.objects.filter(caseid=ids).update(replace_position=replace_position)

        return HttpResponse("编辑成功")
    elif request.method == "POST":
        print("全部修改")
        caseid = request.POST.get("caseID", "")
        casename = request.POST.get("casename", "")
        url = request.POST.get("url", "")
        method = request.POST.get("method", "")
        belong = request.POST.get("belong", "")
        params = request.POST.get("params", "")
        body = request.POST.get("body", "")
        identity = request.POST.get("identity", "")
        isprocess = request.POST.get("isprocess", "")
        dependid = request.POST.get("dependid", "")
        dependkey = request.POST.get("dependkey", "")
        replacekey = request.POST.get("replacekey", "")
        replaceposition = request.POST.get("replaceposition", "")

        ids = request.GET.get("ids", "")
        if "<" in body or ">" in body:
            print('存在需要替换的符号')
            a = body.replace("<", "＜")
            print(a)
            b = a.replace(">", "＞")
            print(b)
            Processapi.objects.filter(caseid=caseid).update(casename=casename, identity=identity, url=url,
                                                            method=method, params=params, body=b, belong=belong,
                                                            isprocess=isprocess, depend_id=dependid,
                                                            depend_key=dependkey,
                                                            replace_key=replacekey, replace_position=replaceposition)
            return HttpResponse("操作成功")
        else:
            Processapi.objects.filter(caseid=caseid).update(casename=casename, identity=identity, url=url,
                                                            method=method, params=params, body=body, belong=belong,
                                                            isprocess=isprocess, depend_id=dependid,
                                                            depend_key=dependkey,
                                                            replace_key=replacekey, replace_position=replaceposition)
            return HttpResponse("操作成功")


# 执行用例-new版本
@login_required
def run_processcase_views(request):
    #全局变量进度
    global num_progress
    content = request.POST.get("request", "")
    content = json.loads(content)
    if len(content) == 1:
        caseid = content[0].get("caseid", "")  # 接口id
        identity = content[0].get("identity", "")  # 用户身份
        Runmethod = RequestMethod(identity)  # 根据用户身份获取请求头Token数据
        url = content[0].get("url", "")  # 登录地址
        casename = content[0].get("casename", "")  # 接口名
        method = content[0].get("method", "")  # 请求方式
        params = content[0].get("params", "")  # query数据
        body = content[0].get("body", "")  # body数据
        isprocess = content[0].get("isprocess", "")  # 是否存在依赖
        # depend_id = content[0].get("depend_id", "")  # 依赖的ID
        # depend_key = content[0].get("depend_key", "")  # 依=依赖的key
        # replace_key = content[0].get("replace_key", "")  # 替换的key
        # replace_position = content[0].get("replace_position", "")  # 替换的位置
        if isprocess == "True":
            return JsonResponse({"status_code": 500, "msg": "我是流程接口，请选择我和我依赖的接口一起运行，依赖的接口响应内容可能有变动，需要一同再次发送请求"})
        # 获取开始运行的时间
        starttime = time.time()
        if "＜" in body or "＞" in body:
            print('body存在需要替换的符号')
            a = body.replace("＜", "<")
            b = a.replace("＞", ">")
            body = b
        try:
            response = Runmethod.run_main(method, url, params, body)
            # 获取运行完的时间
            endtime = time.time()
            runtime = round(endtime - starttime, 3)
            # 存为字典，转换为json格式
            d = {}
            d[casename] = response
            # json格式化
            djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
            print(djson)
            if "身份认证失败" in djson:
                return JsonResponse({"status_code": 401, "msg": "'AccessKey' 或 'AccessToken' 不正确。"})
            if "<" in djson or ">" in djson:
                print('result存在需要替换的符号')
                a = djson.replace("<", "＜")
                b = a.replace(">", "＞")
                Processapi.objects.filter(caseid=content[0]["caseid"]).update(result=b)
            else:
                Processapi.objects.filter(caseid=content[0]["caseid"]).update(result=djson)
            Processapi.objects.filter(caseid=content[0]["caseid"]).update(duration=runtime)
            return HttpResponse(djson)
        # 异常捕获
        except TypeError as e:
            print(e)
            print(type(e))
            return JsonResponse({"status_code": 500, "msg": "异常的id为:"+str(caseid)+","+casename+"操作或函数应用于不适当类型的对象"})
        except json.decoder.JSONDecodeError as e:
            print(e)
            print(type(e))
            return JsonResponse({"status_code": 500, "msg": "异常的id为:"+str(caseid)+","+casename+"json.loads()读取字符串报错"})

    else:
        #多个接口测试的情况
        print("多个接口测试")
        # 将每次运行的字典结果集用列表存储
        L = []
        num = 0
        failed_num = 0
        process_ids = []
        for i in content:
            caseid = i.get("caseid","")
            identity = i.get("identity", "")  # 用户身份
            Runmethod = RequestMethod(identity)  # 根据用户身份获取请求头Token数据
            url = i.get("url", "")  # 登录地址
            method = i.get("method", "")  # 请求方式
            params = i.get("params", "")  # query数据
            body = i.get("body", "")  # body数据
            casename = i.get("casename", "")  # 接口名
            isprocess = i.get("isprocess", "")  # 是否存在依赖
            depend_id = i.get("depend_id", "")  # 依赖的id
            depend_key = i.get("depend_key", "")  # 依赖的键
            replace_key = i.get("replace_key", "")  # 需要替换的键
            replace_position = i.get("replace_position", "")  # 替换的区域
            starttime = time.time()
            # 判断是否为流程测试接口，如果是的话先通过依赖数据的ID查询结果
            if isprocess == "True":
                print("我需要依赖别的接口哦！！！")
                depend_id = depend_id.split(",")

                #如果请求的依赖接口只有一个的时候
                if len(depend_id) == 1:
                    if int(depend_id[0]) in process_ids:
                        print("我所依赖的接口出错了哦")
                        response = "我所依赖的id为"+ depend_id[0] + "的接口出错了哦"
                    else:
                        dependid = Processapi.objects.get(caseid=depend_id[0])
                        # 获取依赖接口返回的结果
                        result = json.loads(dependid.result)[dependid.casename]
                        body = json.loads(body) if body != "" else body
                        params = json.loads(params) if params != "" else params
                        #从前台拿到需替换的key,转为字典，字典的键存入列表
                        replaceKey = eval(replace_key)
                        replaceKey_key = [x for x in replaceKey]
                        print(replaceKey_key)
                        #从前台拿到需要依赖的key,转为字典，把字典的键存入列表
                        dependkey = eval(depend_key)
                        dependkey_key = [x for x in dependkey]
                        print(dependkey_key)
                        #判断替换的区域是body还是params，赋值给变量params_body
                        params_body = params if replace_position == "params" else body
                        depend_value = []   #首先创建依赖的空列表
                        replace_value = []  #首先创建替换的空列表
                        try:
                            for i in range(len(dependkey)):
                                #将依赖的结果集放入一个列表存储
                                dependvalue = jsonpath.jsonpath(result,dependkey_key[i])[dependkey[dependkey_key[i]]]
                                print(dependvalue)
                                if type(dependvalue) is list:
                                    dependvalue = dependvalue[0]
                                depend_value.append(dependvalue)
                                #将需要替换的结果集放入一个列表存储
                                replacevalue = jsonpath.jsonpath(params_body,replaceKey_key[i])[replaceKey[replaceKey_key[i]]]
                                print(replacevalue)
                                if type(replacevalue) is list:
                                    replacevalue = replacevalue[0]
                                replace_value.append(replacevalue)
                            #将变量params_body转为json字符串，为了之后的字符串替换
                            params_body = json.dumps(params_body, ensure_ascii=False, sort_keys=True, indent=2)
                            #将替换的内容体中需要替换的结果集内逐一遍历替换为依赖的结果集内对应的数据
                            for i in range(len(depend_value)):
                                params_body = params_body.replace(replace_value[i],depend_value[i])
                            print(params_body)
                            response = Runmethod.run_main(method, url, params_body, json.dumps(body)) if replace_position =="params" else Runmethod.run_main(method, url, json.dumps(params),params_body)
                        except TypeError as e:
                            print("类型错误")
                            print(e)
                            response = "异常的id为:"+str(caseid)+","+"操作或函数应用于不适当类型的对象"
                        except json.decoder.JSONDecodeError as e:
                            print("json解析错误")
                            print(e)
                            response = "异常的id为:"+str(caseid)+","+"json.loads()读取字符串报错"
                #如果请求的依赖接口不止有一个的时候
                else:
                    body = json.loads(body) if body != "" else body
                    params = json.loads(params) if params != "" else params
                    # 从前台拿到需替换的key,转为字典，字典的键存入列表
                    replaceKey = eval(replace_key)
                    replaceKey_key = [x for x in replaceKey]
                    print(replaceKey_key)
                    # 从前台拿到需要依赖的key,转为字典，把字典的键存入列表
                    dependkey = eval(depend_key)
                    #将所有依赖的接口对应的结果的值通过jsonpath[key]替换出来，加入一个列表中
                    depend_value = []
                    for a in range(len(depend_id)):
                        if int(depend_id[a]) in process_ids:
                            response = "我所依赖的id为" + depend_id[a] + "的接口出错了哦"
                            break
                        else:
                            try:
                                for i in range(len(depend_id)):
                                    dependid = Processapi.objects.get(caseid=depend_id[i])
                                    # 通过id获取依赖接口返回的结果
                                    result = json.loads(dependid.result)[dependid.casename]
                                    print(result)
                                    #获取需要替换的jsonpath[key]的结果，转为字典，字典的键放入一个列表存储。
                                    dependkey_a = dependkey[i]
                                    print(dependkey_a)
                                    dependkey_ab = [x for x in dependkey_a]
                                    print(dependkey_ab)
                                    #
                                    for ii in range(len(dependkey_ab)):
                                        dependvalue = jsonpath.jsonpath(result,dependkey_ab[ii])[dependkey_a[dependkey_ab[ii]]]
                                        print(dependvalue)
                                        if type(dependvalue) is list:
                                            dependvalue = dependvalue[0]
                                        depend_value.append(dependvalue)

                                params_body = params if replace_position == "params" else body
                                print("体内容取值开开始。。。。")
                                replace_value = []
                                for i in range(len(replaceKey_key)):
                                    replacevalue = jsonpath.jsonpath(params_body,replaceKey_key[i])[replaceKey[replaceKey_key[i]]]
                                    print(replacevalue)
                                    if type(replacevalue) is list:
                                        replacevalue = replacevalue[0]
                                    replace_value.append(replacevalue)
                                print(replace_value)
                                # 将变量params_body转为json字符串，为了之后的字符串替换
                                params_body = json.dumps(params_body, ensure_ascii=False, sort_keys=True, indent=2)
                                # 将替换的内容体中需要替换的结果集内逐一遍历替换为依赖的结果集内对应的数据
                                for i in range(len(depend_value)):
                                    params_body = params_body.replace(replace_value[i],depend_value[i])
                                print(params_body)
                                response = Runmethod.run_main(method, url, params_body, json.dumps(body)) if replace_position =="params" else Runmethod.run_main(method, url, json.dumps(params),params_body)

                            except TypeError as e:
                                print("类型错误")
                                print(e)
                                response = "异常的id为:" + str(caseid) + "," + "操作或函数应用于不适当类型的对象"
                            except json.decoder.JSONDecodeError as e:
                                print("json解析错误")
                                print(e)
                                response = "异常的id为:" + str(caseid) + "," + "json.loads()读取字符串报错"
                            break

            # 不需要别的接口
            elif isprocess != "True":
                print("我不需要依赖别的接口！！！")
                if "＜" in body or "＞" in body:
                    print('body存在需要替换的符号')
                    a = body.replace("＜", "<")
                    b = a.replace("＞", ">")
                    body = b
                try:
                    response = Runmethod.run_main(method, url, params, body)
                    # 异常捕获
                except TypeError as e:
                    print(e)
                    response = "异常的id为:" + str(caseid) + "," + "操作或函数应用于不适当类型的对象"
                except json.decoder.JSONDecodeError as e:
                    print(e)
                    response = "异常的id为:" + str(caseid) + "," + "json.loads()读取字符串报错"
                # 获取运行完的时间
            endtime = time.time()
            runtime = round(endtime - starttime, 3)
            # 存为字典，转换为json格式
            print(process_ids)
            d = {}
            d[casename] = response
            djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
            print(djson)
            if "身份认证失败" in djson:
                num_progress = 100
                return JsonResponse({"status_code": 401, "msg": "'AccessKey' 或 'AccessToken' 不正确。"})
            if "error" in djson and "timestamp" in djson or "异常的id为" in djson or "我所依赖的id为" in djson:
                failed_num += 1
                L.append(d)
                process_ids.append(caseid)
                print(process_ids)

            if "<" in djson or ">" in djson:
                print('result存在需要替换的符号')
                a = djson.replace("<", "＜")
                b = a.replace(">", "＞")
                Processapi.objects.filter(caseid=caseid).update(result=b)
            else:
                Processapi.objects.filter(caseid=caseid).update(result=djson)
            Processapi.objects.filter(caseid=caseid).update(duration=runtime)
            num += 1
            #给全局变量每次循环完赋值,取整
            num_progress = round(num/len(content) * 100,)

        dic = {}
        dic["执行接口总数"] = len(content)
        dic["通过接口数"] = len(content) - failed_num
        dic["失败接口数"] = failed_num
        dic["失败接口响应结果集"] = L
        djson_new = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=2)
        return HttpResponse(djson_new)


#进度条
@login_required
def show_progress_views(request):
    global num_progress
    print('show_progress----------'+str(num_progress))
    #当进度百分百的时候，需要吧全局变量初始化，以便下次请求的时候进度条是重0开始，否则默认都是百分之百了
    if num_progress == 100:
        num_progress = 0
        return JsonResponse(100, safe=False)
    #当进度不是百分之百的时候，返回当前进度
    else:
        return JsonResponse(num_progress, safe=False)

#流程测试接口详情
@login_required
def detail_process_api_views(request):
    res = request.GET.get("id", "")
    id = Processapi.objects.get(caseid=res)
    identity = id.identity
    url = id.url
    method = id.method
    params = id.params
    body = id.body
    casename = id.casename
    head = id.exceptres
    belong = id.belong
    result = id.result

    if identity == "sysadmin":
        identity = "系统管理员"
    elif identity == "admin":
        identity = "单位管理员"
    elif identity == "ast":
        identity = "单位档案员"
    elif identity == "transferadmin":
        identity = "数据管理员"
    elif identity == "tdradmin":
        identity = "谢云峰"
    dic = {
        "identity": identity,
        "belong": belong,
        "casename": casename,
        "url": url,
        "method": method,
        "params": params,
        "body": body,
        "result": result,
        "head": head
    }
    return render(request, "detail.html", {"dic": dic})


# 定时任务
@login_required
def timetask_views(request):
    # 获取开始运行的时间
    # start_time = request.POST.get("date", "")
    # 获取结束运行的时间
    end = request.POST.get("date1","")
    end_split = end[11:].split(":")
    end_time = int(end_split[0]) * 60 * 60 + int(end_split[1]) * 60 + int(end_split[2])
    print(end_time)
    # 获取运行的时间间隔
    interval_time = request.POST.get("date2", "")
    interval_time_l = interval_time.split(":")
    interval_time_sjc = int(interval_time_l[0]) * 60 * 60 + int(interval_time_l[1]) * 60 + int(interval_time_l[2])
    # 获取执行的用例列表
    ids = request.POST.get("caseid", "").split(",")[:-1]
    sched = BackgroundScheduler()
    # sched.add_job(job_function, args=(ids,), start_date=start_time, end_date=end_time, trigger=IntervalTrigger(seconds=interval_time_sjc))
    sched.add_job(job_function, "interval",seconds = interval_time_sjc,args=(ids,end_time,sched))
    sched.start()
    # send_ding("定时任务开始,错误的消息才会@各位")
    return HttpResponse("定时任务在后台已经开始,接口出错将由钉钉通知！")


#定时任务job
def job_function(ids,end_time,sched):
    GetToken("sysadmin").get_token_by_role("sysadmin")
    GetToken("ast").get_token_by_role("ast")
    locals_time= datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')[11:]
    locals_time_l = locals_time.split(":")
    locals_time_sjc = int(locals_time_l[0]) * 60 * 60 + int(locals_time_l[1]) * 60 + int(locals_time_l[2])
    print("现在时间:"+str(locals_time_sjc)+"-------"+"结束时间:"+str(end_time))
    if locals_time_sjc <= end_time:
        if len(ids) == 1:
            print("单一接口测试")
            content = ids[0]
            id = Processapi.objects.get(caseid=content)
            identity = id.identity
            url = id.url
            method = id.method
            params = id.params
            body = id.body
            isprocess = id.isprocess
            casename = id.casename
            head = id.header
            Runmethod = RequestMethod(identity)
            if isprocess == "True":
                return JsonResponse({"status_code": 500, "msg": "我是流程接口，请选择我和我依赖的接口一起运行，依赖的接口响应内容可能有变动，需要一同再次发送请求"})

            # 获取开始运行的时间
            starttime = time.time()
            if "＜" in body or "＞" in body:
                print('body存在需要替换的符号')
                a = body.replace("＜", "<")
                b = a.replace("＞", ">")
                body = b
            try:
                response = Runmethod.run_main(method, url, params, body)
                # 获取运行完的时间
                endtime = time.time()
                runtime = round(endtime - starttime, 3)
                # 存为字典，转换为json格式
                d = {}
                d[casename] = response
                # json格式化
                djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
                print(djson)
                if "身份认证失败" in djson:
                    return JsonResponse({"status_code": 401, "msg": "身份认证失败。 'AccessKey' 或 'AccessToken' 不正确。"})
                if "<" in djson or ">" in djson:
                    print('result存在需要替换的符号')
                    a = djson.replace("<", "＜")
                    b = a.replace(">", "＞")
                    Processapi.objects.filter(caseid=content).update(result=b)

                else:
                    Processapi.objects.filter(caseid=content).update(result=djson)
                Processapi.objects.filter(caseid=content).update(duration=runtime)
                # return HttpResponse(djson)
            # 异常捕获
            except TypeError as e:
                print(e)
                send_ding("异常的id为:"+str(content)+","+"操作或函数应用于不适当类型的对象",head)
                send_link(content, "{" + casename + "-详情}-->")
                # return JsonResponse({"status_code": 500, "msg": "操作或函数应用于不适当类型的对象"})
            except json.decoder.JSONDecodeError as e:
                print(e)
                # return JsonResponse({"status_code": 500, "msg": "json.loads()读取字符串报错"})
                send_ding("异常的id为:"+str(content)+","+"json.loads()读取字符串报错",head)
                send_link(content, "{" + casename + "-详情}-->")
        else:
            print("多个接口测试")

            # 将每次运行的字典结果集用列表存储
            L = []
            failed_num = 0
            process_ids = []
            for ucaseid in ids:
                id = Processapi.objects.get(caseid=ucaseid)
                identity = id.identity
                url = id.url
                method = id.method
                params = id.params
                body = id.body
                casename = id.casename
                isprocess = id.isprocess
                depend_id = id.depend_id
                depend_key = id.depend_key
                replace_key = id.replace_key
                replace_position = id.replace_position
                head = id.header
                Runmethod = RequestMethod(identity)
                starttime = time.time()

                # 判断是否为流程测试接口，如果是的话先通过依赖数据的ID查询结果
                if isprocess == "True":
                    print("我需要依赖别的接口哦！！！")
                    depend_id = depend_id.split(",")

                    # 如果请求的依赖接口只有一个的时候
                    if len(depend_id) == 1:
                        if int(depend_id[0]) in process_ids:
                            print("我所依赖的接口出错了哦")
                            response = "我所依赖的id为" + depend_id[0] + "的接口出错了哦"
                        else:
                            dependid = Processapi.objects.get(caseid=depend_id[0])
                            # 获取依赖接口返回的结果
                            result = json.loads(dependid.result)[dependid.casename]
                            body = json.loads(body) if body != "" else body
                            params = json.loads(params) if params != "" else params
                            # 从前台拿到需替换的key,转为字典，字典的键存入列表
                            replaceKey = eval(replace_key)
                            replaceKey_key = [x for x in replaceKey]
                            print(replaceKey_key)
                            # 从前台拿到需要依赖的key,转为字典，把字典的键存入列表
                            dependkey = eval(depend_key)
                            dependkey_key = [x for x in dependkey]
                            print(dependkey_key)
                            # 判断替换的区域是body还是params，赋值给变量params_body
                            params_body = params if replace_position == "params" else body
                            depend_value = []  # 首先创建依赖的空列表
                            replace_value = []  # 首先创建替换的空列表
                            try:
                                for i in range(len(dependkey)):
                                    # 将依赖的结果集放入一个列表存储
                                    dependvalue = jsonpath.jsonpath(result, dependkey_key[i])[
                                        dependkey[dependkey_key[i]]]
                                    print(dependvalue)
                                    if type(dependvalue) is list:
                                        dependvalue = dependvalue[0]
                                    depend_value.append(dependvalue)
                                    # 将需要替换的结果集放入一个列表存储
                                    replacevalue = jsonpath.jsonpath(params_body, replaceKey_key[i])[
                                        replaceKey[replaceKey_key[i]]]
                                    print(replacevalue)
                                    if type(replacevalue) is list:
                                        replacevalue = replacevalue[0]
                                    replace_value.append(replacevalue)
                                # 将变量params_body转为json字符串，为了之后的字符串替换
                                params_body = json.dumps(params_body, ensure_ascii=False, sort_keys=True, indent=2)
                                # 将替换的内容体中需要替换的结果集内逐一遍历替换为依赖的结果集内对应的数据
                                for i in range(len(depend_value)):
                                    params_body = params_body.replace(replace_value[i], depend_value[i])
                                print(params_body)
                                response = Runmethod.run_main(method, url, params_body, json.dumps(
                                    body)) if replace_position == "params" else Runmethod.run_main(method, url,
                                                                                                   json.dumps(params),
                                                                                                   params_body)
                            except TypeError as e:
                                print("类型错误")
                                print(e)
                                response = "异常的id为:" + str(ucaseid) + "," + "操作或函数应用于不适当类型的对象"
                            except json.decoder.JSONDecodeError as e:
                                print("json解析错误")
                                print(e)
                                response = "异常的id为:" + str(ucaseid) + "," + "json.loads()读取字符串报错"
                    # 如果请求的依赖接口不止有一个的时候
                    else:
                        body = json.loads(body) if body != "" else body
                        params = json.loads(params) if params != "" else params
                        # 从前台拿到需替换的key,转为字典，字典的键存入列表
                        replaceKey = eval(replace_key)
                        replaceKey_key = [x for x in replaceKey]
                        print(replaceKey_key)
                        # 从前台拿到需要依赖的key,转为字典，把字典的键存入列表
                        dependkey = eval(depend_key)
                        # 将所有依赖的接口对应的结果的值通过jsonpath[key]替换出来，加入一个列表中
                        depend_value = []
                        for a in range(len(depend_id)):
                            if int(depend_id[a]) in process_ids:
                                response = "我所依赖的id为" + depend_id[a] + "的接口出错了哦"
                                break
                            else:
                                try:
                                    for i in range(len(depend_id)):
                                        dependid = Processapi.objects.get(caseid=depend_id[i])
                                        # 通过id获取依赖接口返回的结果
                                        result = json.loads(dependid.result)[dependid.casename]
                                        print(result)
                                        # 获取需要替换的jsonpath[key]的结果，转为字典，字典的键放入一个列表存储。
                                        dependkey_a = dependkey[i]
                                        print(dependkey_a)
                                        dependkey_ab = [x for x in dependkey_a]
                                        print(dependkey_ab)
                                        #
                                        for ii in range(len(dependkey_ab)):
                                            dependvalue = jsonpath.jsonpath(result, dependkey_ab[ii])[
                                                dependkey_a[dependkey_ab[ii]]]
                                            print(dependvalue)
                                            if type(dependvalue) is list:
                                                dependvalue = dependvalue[0]
                                            depend_value.append(dependvalue)

                                    params_body = params if replace_position == "params" else body
                                    print("体内容取值开开始。。。。")
                                    replace_value = []
                                    for i in range(len(replaceKey_key)):
                                        replacevalue = jsonpath.jsonpath(params_body, replaceKey_key[i])[
                                            replaceKey[replaceKey_key[i]]]
                                        print(replacevalue)
                                        if type(replacevalue) is list:
                                            replacevalue = replacevalue[0]
                                        replace_value.append(replacevalue)
                                    print(replace_value)
                                    # 将变量params_body转为json字符串，为了之后的字符串替换
                                    params_body = json.dumps(params_body, ensure_ascii=False, sort_keys=True, indent=2)
                                    # 将替换的内容体中需要替换的结果集内逐一遍历替换为依赖的结果集内对应的数据
                                    for i in range(len(depend_value)):
                                        params_body = params_body.replace(replace_value[i], depend_value[i])
                                    print(params_body)
                                    response = Runmethod.run_main(method, url, params_body, json.dumps(
                                        body)) if replace_position == "params" else Runmethod.run_main(method, url,
                                                                                                       json.dumps(
                                                                                                           params),
                                                                                                       params_body)

                                except TypeError as e:
                                    print("类型错误")
                                    print(e)
                                    response = "异常的id为:" + str(ucaseid) + "," + "操作或函数应用于不适当类型的对象"
                                except json.decoder.JSONDecodeError as e:
                                    print("json解析错误")
                                    print(e)
                                    response = "异常的id为:" + str(ucaseid) + "," + "json.loads()读取字符串报错"
                                break

                # 不需要别的接口
                elif isprocess != "True":
                    print("我不需要依赖别的接口！！！")
                    if "＜" in body or "＞" in body:
                        print('body存在需要替换的符号')
                        a = body.replace("＜", "<")
                        b = a.replace("＞", ">")
                        body = b
                    try:
                        response = Runmethod.run_main(method, url, params, body)
                        # 异常捕获
                    except TypeError as e:
                        print(e)
                        response = "异常的id为:" + str(ucaseid) + "," + "操作或函数应用于不适当类型的对象"
                    except json.decoder.JSONDecodeError as e:
                        print(e)
                        response = "异常的id为:" + str(ucaseid) + "," + "json.loads()读取字符串报错"
                    # 获取运行完的时间
                # 获取运行完的时间
                endtime = time.time()
                runtime = round(endtime - starttime - 0.015, 3)
                # 存为字典，转换为json格式
                d = {}
                d[casename] = response
                # json格式化
                djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
                print(djson)
                if "error" in djson and "timestamp" in djson or "异常的id为" in djson or "我所依赖的id为" in djson:
                    failed_num += 1
                    L.append(d)
                    process_ids.append(ucaseid)
                    send_ding(djson,head)
                    send_link(ucaseid,"{"+casename+"-详情}-->")
                if "<" in djson or ">" in djson:
                    print('result存在需要替换的符号')
                    a = djson.replace("<", "＜")
                    b = a.replace(">", "＞")
                    Processapi.objects.filter(caseid=ucaseid).update(result=b)
                    Processapi.objects.filter(caseid=ucaseid).update(duration=runtime)
                else:
                    Processapi.objects.filter(caseid=ucaseid).update(result=djson)
                    Processapi.objects.filter(caseid=ucaseid).update(duration=runtime)
            dic = {}
            dic["执行接口总数"] = len(ids)
            dic["通过接口数"] = len(ids) - failed_num
            dic["失败接口数"] = failed_num
            dic["失败接口响应结果集"] = L
            djson_new = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=2)
            send_ding(djson_new)
    else:
        try:
            print("我是傻逼！")
            sched.shutdown()
            print("定时任务结束")
        except RuntimeError:
            print("我是傻逼！")
            send_ding("{come over...定时任务结束}")
            pass
        except Exception as e:
            print(e)
            send_ding("{come over...定时任务结束}")


#排序
@login_required
def process_sort_views(request):
    if request.method == "GET":
        oldIndex = int(request.GET.get("oldIndex",""))+1
        newIndex = int(request.GET.get("newIndex", ""))+1
        if oldIndex < newIndex:
            q = []
            for i in range(oldIndex,newIndex):
                a = i + 1
                for b in Processapi.objects.filter(sortid=a):
                    q.append(b.caseid)
                Processapi.objects.filter(sortid=a).update(sortid=i)
            l = Processapi.objects.filter(sortid=oldIndex)
            for lll in l:
                if lll.caseid not in q:
                    Processapi.objects.filter(caseid=lll.caseid).update(sortid=newIndex)
        elif oldIndex > newIndex:
            Processapi.objects.filter(sortid=oldIndex).update(sortid=-1)
            L = []
            for i in range(newIndex,oldIndex):
                L.append(i)
            e = L[::-1]
            for r in e:
                Processapi.objects.filter(sortid=r).update(sortid=r+1)
            Processapi.objects.filter(sortid=-1).update(sortid=newIndex)
        return HttpResponse("排序成功")
    else:
        data = request.POST.get("data","")
        belong = request.POST.get("belong","")
        system = request.POST.get("system", "")
        datas = json.loads(data)

        if belong:
            all = Processapi.objects.filter(Q(belong=belong) & Q(system=system))
        else:
            all = Processapi.objects.filter(system=system)

        l = []
        for i in all:
            l.append(i.sortid)
        l.sort()
        flag = 0
        for d in datas:
            Processapi.objects.filter(caseid=d).update(sortid=l[flag])
            flag += 1
        return HttpResponse("排序成功")



#多线程运行
def repeatrun_views(request):
    global thread_dict
    content = request.POST.get("request", "")
    content = json.loads(content)
    iterations = request.POST.get("runtime","")
    concurrency = request.POST.get("concurrency","")
    print(content)
    print(iterations)
    print(concurrency)

    if concurrency == "" or int(concurrency) == 1:
        L = {0:int(iterations)}
        thread = []
        for start,end in L.items():
            t = threading.Thread(target=run_apicase,args=(start,end,content))
            thread.append(t)

        starttime = time.time()
        for i in range(len(thread)):
            thread[i].start()

        for w in range(len(thread)):
            thread[w].join()
        endtime = time.time()

        runtime = round(endtime - starttime, 3)
        print(runtime)
        # q = time.time()
        # print(run_apicase(start,end,content))
        # w = time.time()
        # print(round(w - q, 3))
        print("运行已结束")
        thread_json = json.dumps(thread_dict, ensure_ascii=False, sort_keys=True, indent=2)
        thread_dict = {}
        return HttpResponse(thread_json)

        # return JsonResponse({"status_code": 200, "msg": "运行已结束,运行时间为:"+str(runtime)+"秒"})


def run_apicase(start,end,content):
    global num_progress
    global thread_dict
    failed_num = 0
    if len(content) == 1:
        caseid = content[0].get("caseid", "")  # 接口id
        identity = content[0].get("identity", "")  # 用户身份
        Runmethod = RequestMethod(identity)  # 根据用户身份获取请求头Token数据
        url = content[0].get("url", "")  # 登录地址
        casename = content[0].get("casename", "")  # 接口名
        method = content[0].get("method", "")  # 请求方式
        params = content[0].get("params", "")  # query数据
        body = content[0].get("body", "")  # body数据
        isprocess = content[0].get("isprocess", "")  # 是否存在依赖

        if isprocess == "True":
            thread_dict = {"status_code": 500, "msg": "我是流程接口，请选择我和我依赖的接口一起运行，依赖的接口响应内容可能有变动，需要一同再次发送请求"}
            return thread_dict

        # 获取开始运行的时间
        if "＜" in body or "＞" in body:
            print('body存在需要替换的符号')
            a = body.replace("＜", "<")
            b = a.replace("＞", ">")
            body = b
        try:
            L = []
            a = time.time()
            for num in range(start, end):
                d = {}
                starttime = time.time()
                response = Runmethod.run_main(method, url, params, body)
                print(response)
                d[casename] = response
                endtime = time.time()
                runtime = round(endtime - starttime, 3)
                print(runtime)
                d["响应时间"] = str(runtime)
                num += 1
                # 给全局变量每次循环完赋值,取整
                num_progress = round(num / end * 100, )
                # json格式化
                djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
                print(djson)
                if "身份认证失败" in djson:
                    num_progress = 100
                    thread_dict["status_code"] = 401
                    thread_dict["msg"] = "'AccessKey' 或 'AccessToken' 不正确。"

                if "error" in djson and "timestamp" in djson:
                    failed_num += 1
                    L.append(d)

                if "<" in djson or ">" in djson:
                    print('result存在需要替换的符号')
                    a = djson.replace("<", "＜")
                    b = a.replace(">", "＞")
                    Processapi.objects.filter(caseid=caseid).update(result=b)
                else:
                    Processapi.objects.filter(caseid=caseid).update(result=djson)
                Processapi.objects.filter(caseid=caseid).update(result=djson)

            b = time.time()
            c = round(b - a, 3)
            thread_dict["总消耗时间"] = c
            thread_dict["执行接口总数"] = end
            thread_dict["通过接口数"] = end - failed_num
            thread_dict["失败接口数"] = failed_num
            thread_dict["失败接口响应结果集"] = L
            thread_dict["重复执行次数"] = end
            # 发送钉钉消息
            # send_ding(djson_new)
            return thread_dict

        except TypeError as e:
            print(e)
            thread_dict["类型错误"] = "异常的id为:"+caseid+","+casename+"操作或函数应用于不适当类型的对象"
            return thread_dict
        except json.decoder.JSONDecodeError as e:
            print(e)
            thread_dict["JSON解析异常"] = "异常的id为:"+caseid+","+casename+"操作或函数应用于不适当类型的对象"
            return thread_dict

    else:
        # 多个接口测试的情况
        print("多个接口测试")
        # 将每次运行的字典结果集用列表存储
        L = []
        t1 = time.time()
        cnt = 0
        process_ids = []
        for num in range(start, end):
            for i in content:
                caseid = i.get("caseid","")
                identity = i.get("identity", "")  # 用户身份
                Runmethod = RequestMethod(identity)  # 根据用户身份获取请求头Token数据
                url = i.get("url", "")  # 登录地址
                method = i.get("method", "")  # 请求方式
                params = i.get("params", "")  # query数据
                body = i.get("body", "")  # body数据
                casename = i.get("casename", "")  # 接口名
                isprocess = i.get("isprocess", "")  # 是否存在依赖
                depend_id = i.get("depend_id", "")  # 依赖的id
                depend_key = i.get("depend_key", "")  # 依赖的键
                replace_key = i.get("replace_key", "")  # 需要替换的键
                replace_position = i.get("replace_position", "")  # 替换的区域

                starttime = time.time()
                #判断是否为流程测试接口，如果是的话先通过依赖数据的ID查询结果
                if isprocess == "True":
                    print("我需要依赖别的接口哦！！！")
                    depend_id = depend_id.split(",")
                    #如果请求的依赖接口只有一个的时候
                    if len(depend_id) == 1:
                        if int(depend_id[0]) in process_ids:
                            print("我所依赖的接口出错了哦")
                            response = "我所依赖的id为" + depend_id[0] + "的接口出错了哦"
                        else:
                            dependid = Processapi.objects.get(caseid=depend_id[0])
                            # 获取依赖接口返回的结果
                            result = json.loads(dependid.result)[dependid.casename]
                            body = json.loads(body) if body != "" else body
                            params = json.loads(params) if params != "" else params
                            #从前台拿到需替换的key,转为字典，字典的键存入列表
                            replaceKey = eval(replace_key)
                            replaceKey_key = [x for x in replaceKey]
                            print(replaceKey_key)
                            #从前台拿到需要依赖的key,转为字典，把字典的键存入列表
                            dependkey = eval(depend_key)
                            dependkey_key = [x for x in dependkey]
                            print(dependkey_key)
                            #判断替换的区域是body还是params，赋值给变量params_body
                            params_body = params if replace_position == "params" else body
                            depend_value = []   #首先创建依赖的空列表
                            replace_value = []  #首先创建替换的空列表
                            try:
                                for i in range(len(dependkey)):
                                    #将依赖的结果集放入一个列表存储
                                    dependvalue = jsonpath.jsonpath(result,dependkey_key[i])[dependkey[dependkey_key[i]]]
                                    print(dependvalue)
                                    if type(dependvalue) is list:
                                        dependvalue = dependvalue[0]
                                    depend_value.append(dependvalue)
                                    #将需要替换的结果集放入一个列表存储
                                    replacevalue = jsonpath.jsonpath(params_body,replaceKey_key[i])[replaceKey[replaceKey_key[i]]]
                                    print(replacevalue)
                                    if type(replacevalue) is list:
                                        replacevalue = replacevalue[0]
                                    replace_value.append(replacevalue)
                                #将变量params_body转为json字符串，为了之后的字符串替换
                                params_body = json.dumps(params_body, ensure_ascii=False, sort_keys=True, indent=2)
                                #将替换的内容体中需要替换的结果集内逐一遍历替换为依赖的结果集内对应的数据
                                for i in range(len(depend_value)):
                                    params_body = params_body.replace(replace_value[i],depend_value[i])
                                print(params_body)
                                response = Runmethod.run_main(method, url, params_body, json.dumps(body)) if replace_position =="params" else Runmethod.run_main(method, url, json.dumps(params),params_body)
                            except TypeError as e:
                                print(e)
                                response = "异常的id为:" + str(caseid) + "," + "操作或函数应用于不适当类型的对象"
                            except json.decoder.JSONDecodeError as e:
                                print(e)
                                num_progress = 100
                                response = "异常的id为:" + str(caseid) + "," + "json.loads()读取字符串报错"
                    #如果请求的依赖接口不止有一个的时候
                    else:
                        body = json.loads(body) if body != "" else body
                        params = json.loads(params) if params != "" else params
                        # 从前台拿到需替换的key,转为字典，字典的键存入列表
                        replaceKey = eval(replace_key)
                        replaceKey_key = [x for x in replaceKey]
                        print(replaceKey_key)
                        # 从前台拿到需要依赖的key,转为字典，把字典的键存入列表
                        dependkey = eval(depend_key)
                        # 将所有依赖的接口对应的结果的值通过jsonpath[key]替换出来，加入一个列表中
                        depend_value = []
                        for a in range(len(depend_id)):
                            if int(depend_id[a]) in process_ids:
                                response = "我所依赖的id为" + depend_id[0] + "的接口出错了哦"
                                break
                            else:
                                try:
                                    for i in range(len(depend_id)):
                                        dependid = Processapi.objects.get(caseid=depend_id[i])
                                        # 通过id获取依赖接口返回的结果
                                        result = json.loads(dependid.result)[dependid.casename]
                                        print(result)
                                        # 获取需要替换的jsonpath[key]的结果，转为字典，字典的键放入一个列表存储。
                                        dependkey_a = dependkey[i]
                                        print(dependkey_a)
                                        dependkey_ab = [x for x in dependkey_a]
                                        print(dependkey_ab)
                                        #
                                        for ii in range(len(dependkey_ab)):
                                            dependvalue = jsonpath.jsonpath(result, dependkey_ab[ii])[
                                                dependkey_a[dependkey_ab[ii]]]
                                            print(dependvalue)
                                            if type(dependvalue) is list:
                                                dependvalue = dependvalue[0]
                                            depend_value.append(dependvalue)

                                    params_body = params if replace_position == "params" else body
                                    print("体内容取值开开始。。。。")
                                    replace_value = []
                                    for i in range(len(replaceKey_key)):
                                        replacevalue = jsonpath.jsonpath(params_body, replaceKey_key[i])[
                                            replaceKey[replaceKey_key[i]]]
                                        print(replacevalue)
                                        if type(replacevalue) is list:
                                            replacevalue = replacevalue[0]
                                        replace_value.append(replacevalue)
                                    print(replace_value)
                                    # 将变量params_body转为json字符串，为了之后的字符串替换
                                    params_body = json.dumps(params_body, ensure_ascii=False, sort_keys=True, indent=2)
                                    # 将替换的内容体中需要替换的结果集内逐一遍历替换为依赖的结果集内对应的数据
                                    for i in range(len(depend_value)):
                                        params_body = params_body.replace(replace_value[i], depend_value[i])
                                    print(params_body)
                                    response = Runmethod.run_main(method, url, params_body, json.dumps(
                                        body)) if replace_position == "params" else Runmethod.run_main(method, url,
                                                                                                       json.dumps(
                                                                                                           params),
                                                                                                       params_body)

                                except TypeError as e:
                                    print("类型错误")
                                    print(e)
                                    response = "异常的id为:" + str(caseid) + "," + "操作或函数应用于不适当类型的对象"
                                except json.decoder.JSONDecodeError as e:
                                    print("json解析错误")
                                    print(e)
                                    response = "异常的id为:" + str(caseid) + "," + "json.loads()读取字符串报错"
                                break
                #不需要别的接口
                elif isprocess != "True":
                    print("我不需要依赖别的接口！！！")
                    if "＜" in body or "＞" in body:
                        print('body存在需要替换的符号')
                        a = body.replace("＜", "<")
                        b = a.replace("＞", ">")
                        body = b
                    try:
                        response = Runmethod.run_main(method, url, params, body)
                        #异常捕获
                    except TypeError as e:
                        print(e)
                        response = "异常的id为:" + str(caseid) + "," + "操作或函数应用于不适当类型的对象"
                    except json.decoder.JSONDecodeError as e:
                        print(e)
                        response = "异常的id为:" + str(caseid) + "," + "json.loads()读取字符串报错"
                    # 获取运行完的时间
                endtime = time.time()
                runtime = round(endtime - starttime, 3)
                #存为字典，转换为json格式
                d = {}
                d[casename] = response
                #json格式化
                djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
                print(djson)
                if "身份认证失败" in djson:
                    num_progress = 100
                    thread_dict["status_code"] = 401
                    thread_dict["msg"] = "'AccessKey' 或 'AccessToken' 不正确。"
                    return thread_dict

                if "error" in djson and "timestamp" in djson or "异常的id为" in djson or "我所依赖的id为" in djson:
                    failed_num += 1
                    L.append(d)
                    process_ids.append(caseid)
                    print(process_ids)

                if "<" in djson or ">" in djson:
                    print('result存在需要替换的符号')
                    a = djson.replace("<", "＜")
                    b = a.replace(">", "＞")
                    Processapi.objects.filter(caseid=caseid).update(result=b)
                else:
                    Processapi.objects.filter(caseid=caseid).update(result=djson)
                Processapi.objects.filter(caseid=caseid).update(duration=runtime)
                cnt += 1
                #给全局变量每次循环完赋值,取整
                num_progress = round(cnt/(end*len(content)) * 100,)
        t2 = time.time()
        all_time = t2 - t1
        c = round(all_time, 3)
        thread_dict["总消耗时间"] = str(c) + "秒"
        thread_dict["执行接口总数"] = len(content) * end
        thread_dict["通过接口数"] = len(content) * end - failed_num
        thread_dict["失败接口数"] = failed_num
        thread_dict["失败接口响应结果集"] = L
        thread_dict["重复执行次数"] = end
        return thread_dict


