import os
from datetime import datetime
import xlrd
import json
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.shortcuts import render
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import *
from Api.interfacetest.run_method import RequestMethod
from Api.interfacetest.get_header import ReqParam
from Api.webuitest.DingDing import send_ding



#接口api用例首页
def apiindex_view(request):
    id = request.session.get('id')
    uname = User.objects.get(id=id).uname
    a = request.GET.get("belong","")
    case_count = Case.objects.all().count()
    return render(request,"apiindex.html",{"user":uname,"abq":a,"case_count":case_count})



#用例列表
def apilist_view(request):
    casename = request.GET.get("key[casename]","")
    if casename:
        print("搜索的用例名是:"+casename)
    belong = request.GET.get('belong',"")
    print("请求进入的模块是:"+belong)
    if casename == "" and belong == "":
        apilists = Case.objects.filter()


    elif belong == "unit":
        apilists = Case.objects.filter(belong__contains="单位接口")
    elif belong == "dept":
        apilists = Case.objects.filter(belong__contains="部门管理接口")
    elif belong == "user":
        apilists = Case.objects.filter(belong__contains="用户管理接口")
    elif belong == "views":
        apilists = Case.objects.filter(belong__contains="视图管理接口")
    elif belong == "policy":
        apilists = Case.objects.filter(belong__contains="保留处置策略接口")
    elif belong == "role":
        apilists = Case.objects.filter(belong__contains="角色管理接口")
    elif belong == "data_form_config":
        apilists = Case.objects.filter(belong__contains="数据表单配置管理接口")
    elif belong == "category":
        apilists = Case.objects.filter(belong__contains="门类模块接口")
    elif belong == "class":
        apilists = Case.objects.filter(belong__contains="类目模块接口")
    elif belong == "acl":
        apilists = Case.objects.filter(belong__contains="访问控制权限接口")
    elif belong == "view":
        apilists = Case.objects.filter(belong__contains="视图自定义接口")
    elif belong == "record":
        apilists = Case.objects.filter(belong__contains="Record接口")
    elif belong == "document":
        apilists = Case.objects.filter(belong__contains="文档管理接口")
    elif belong == "volume":
        apilists = Case.objects.filter(belong__contains="案卷管理接口")
    elif belong == "archives":
        apilists = Case.objects.filter(belong__contains="档案管理接口")
    elif belong == "resource":
        apilists = Case.objects.filter(belong__contains="资源管理接口")
    elif belong == "navigation":
        apilists = Case.objects.filter(belong__contains="导航管理接口")
    elif belong == "data_form":
        apilists = Case.objects.filter(belong__contains="数据表单管理接口")
    elif belong == "file_plan":
        apilists = Case.objects.filter(belong__contains="文件计划管理接口")
    elif belong == "common":
        apilists = Case.objects.filter(belong__contains="公共操作相关接口")
    elif belong == "common_folder":
        apilists = Case.objects.filter(belong__contains="通用文件夹管理接口")
    elif belong == "metadata":
        apilists = Case.objects.filter(belong__contains="元数据管理平台接口")


    elif casename:
        apilists = Case.objects.filter(casename__contains=casename)
    L = []
    for weblist in apilists:
        data = {
            "caseid": weblist.caseid,
            "identity": weblist.identity,
            "casename": weblist.casename,
            "url": weblist.url,
            "method": weblist.method,
            "params": weblist.params,
            "body": weblist.body,
            "result": weblist.result
        }
        L.append(data)
    print("此模块的用例个数为:"+str(len(L)))
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
def create_apicase_views(request):
    if request.method == 'POST':
        casename = request.POST.get("casename", "")
        url = request.POST.get("url", "")
        method = request.POST.get("method", "")
        belong = request.POST.get("belong", "")
        params = request.POST.get("params", "")
        body = request.POST.get("body", "")
        identity = request.POST.get("identity", "")
        Case.objects.create(casename=casename, identity=identity, url=url,
                               method=method, params=params, body=body, belong=belong)
        return HttpResponseRedirect("/apiindex/")



#删除api用例
def delete_apicase_views(request):
    if request.method == "GET":
        ids = request.GET.get("ids","")
        if ids:
            print(ids)
            Case.objects.filter(caseid=ids).delete()
            return HttpResponse("删除成功")



#更新api用例
def update_apicase_views(request):
    if request.method == "GET":
        params = request.GET.get('params',"")
        body =request.GET.get("body","")
        ids = request.GET.get("ids","")
        print(ids)
        if params:
            print(params)
            if params == "null":
                Case.objects.filter(caseid=ids).update(params="")
            else:
                Case.objects.filter(caseid=ids).update(params=params)

        elif body:
            print(body)
            if body == "null":
                Case.objects.filter(caseid=ids).update(body="")
            else:
                Case.objects.filter(caseid=ids).update(body=body)
        return HttpResponse("编辑成功")


#执行用例
def run_apicase_views(request):
    ids= request.GET.get("caseid").split(",")[:-1]
    print(ids)
    if len(ids) == 1:
        print("单一接口测试")
        d = {}
        for ucaseid in ids:
            id = Case.objects.get(caseid=ucaseid)
            identity = id.identity
            Runmethod = RequestMethod(identity)
            url = "http://demo.amberdata.cn/ermsapi/v2"+id.url
            method = id.method
            params = id.params
            body = id.body
            casename = id.casename
            casename = casename
            #eval()字符串转字典
            starttime = datetime.now()
            if body != "" and params == "":
                body = eval(body)
                response = Runmethod.run_main(method,url,params,body)

            elif body != "" and params != "":
                body = eval(body)
                params = eval(params)
                response = Runmethod.run_main(method,url,params,body)

            elif body == '':
                if params:
                    params = eval(params)
                    response = Runmethod.run_main(method, url, params, body)

                else:
                    response = Runmethod.run_main(method, url, params, body)

            #将结果存到列表返回前端
            # for i in range(1,len(ids)+1):
            #     L.append(str(i)+"."+casename+"---->")
            #     L.append(response)

            #存为字典，转换为json格式
            endtime = datetime.now()
            runtime = endtime - starttime
            print(runtime)

            runtime_a = str(runtime).split('.')
            runtime_b = runtime_a[0].split(":")

            d[casename] = response
            if runtime_b[2] > "00" and runtime_b[2] <= "03":
                d[casename+"---＞"+"运行一般"] = str(runtime)
            elif runtime_b[2] > "03":
                d[casename +"---＞"+ "运行缓慢"] = str(runtime)
            else:
                d[casename +"---＞"+ "运行迅速"] = str(runtime)
            print(d)
            #json格式化
            djson = json.dumps(d, ensure_ascii=False,sort_keys=True, indent=2)
            if "<" in djson or ">" in djson:
                print('存在需要替换的符号')
                a = djson.replace("<","＜")
                print(a)
                b = a.replace(">","＞")
                print(b)
                Case.objects.filter(caseid=ucaseid).update(result=b)
            else:
                Case.objects.filter(caseid=ucaseid).update(result=djson)

        print(djson)
        # print(type(djson))//str
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
            id = Case.objects.get(caseid=ucaseid)
            identity = id.identity
            Runmethod = RequestMethod(identity)
            # Header = ReqParam().get_user_power(identity)['accessToken']
            url = "http://demo.amberdata.cn/ermsapi/v2" + id.url
            method = id.method
            params = id.params
            body = id.body
            casename = id.casename
            casename = casename
            #计算运行前的时间
            starttime = datetime.now()
            if body != "" and params == "":
                # eval()字符串转字典
                body = eval(body)
                response = Runmethod.run_main(method, url, params, body)

            elif body != "" and params != "":
                body = eval(body)
                params = eval(params)
                response = Runmethod.run_main(method, url, params, body)

            elif body == '':
                if params:
                    params = eval(params)
                    response = Runmethod.run_main(method, url, params, body)

                else:
                    response = Runmethod.run_main(method, url, params, body)

            #计算运行结束的时间
            endtime = datetime.now()
            #计算前后两次时间差
            runtime = endtime - starttime
            #获取请求前后的时间差
            print(runtime)


            runtime_a = str(runtime).split('.')
            runtime_b = runtime_a[0].split(":")
            # 所有内容所在一个字典里
            d[casename] = response
            if runtime_b[2] > "00" and runtime_b[2] <= "03":
                d[casename+"---＞"+"运行一般"] = str(runtime)
            elif runtime_b[2] > "03":
                d[casename +"---＞"+ "运行缓慢"] = str(runtime)
            else:
                d[casename +"---＞"+ "运行迅速"] = str(runtime)

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
                Case.objects.filter(caseid=ucaseid).update(result=b)
            else:
                #每次运行结束将每个接口返回的数据JOSN格式化存入数据库
                Case.objects.filter(caseid=ucaseid).update(result=djson)

        #print(L)
        #创建一个字典存储包含所有字典的列表
        dict = {}
        dict["Response"] = L
        #转换为JSON格式，且格式化
        djson_new = json.dumps(dict, ensure_ascii=False, sort_keys=True, indent=2)
        print(djson_new)
        # 发送钉钉消息
        #send_ding(djson_new)
        #将JSON数据返回给前端
        return HttpResponse(djson_new)
