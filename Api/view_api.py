import io
from xlwt import *
import os,sys
import time
from datetime import datetime
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import *
from Api.interfacetest.run_method import RequestMethod
from Api.interfacetest.get_header import  GetToken
from Api.webuitest.DingDing import send_ding

currentUrl = os.path.dirname(__file__)
#父文件路径
cur_path = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(cur_path)
from webuitest.conn_database import ConnDataBase


#接口erms用例首页
@login_required
def apiindex_view(request):
    a = request.GET.get("belong","")
    case_count = Case.objects.filter(system="erms").count()
    return render(request,"apiindex.html",{"user":"朱占豪","abq":a,"case_count":case_count})


#接口transfer用例首页
@login_required
def transferindex_view(request):
    a = request.GET.get("belong","")
    case_count = Case.objects.filter(system="transfer").count()
    return render(request,"transferindex.html",{"user":"朱占豪","abq":a,"case_count":case_count})


#erms用例列表
@login_required
def apilist_view(request):
    casename = request.GET.get("key[casename]","")
    if casename:
        print("搜索的用例名是:"+casename)
    belong = request.GET.get('belong',"")
    print("请求进入的模块是:"+belong)
    if casename == "" and belong == "":
        apilists = Case.objects.filter()

    #流程接口
    elif belong == "process":
        #匹配流程字段的值不能等于空
        apilists = Case.objects.filter(~Q(isprocess= ''))


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


    elif belong == "record_yj":
        apilists = Case.objects.filter(belong__contains="档案管理接口")
    elif belong == "resource_yj":
        apilists = Case.objects.filter(belong__contains="资源管理接口")
    elif belong == "yuwen":
        apilists = Case.objects.filter(belong__contains="导航管理接口")
    elif belong == "navigation_yj":
        apilists = Case.objects.filter(belong__contains="数据表单管理接口")
    elif belong == "comments":
        apilists = Case.objects.filter(belong__contains="文件计划管理接口")
    elif belong == "attribute_mapping_scheme_yj":
        apilists = Case.objects.filter(belong__contains="公共操作相关接口")
    elif belong == "common_folder":
        apilists = Case.objects.filter(belong__contains="通用文件夹管理接口")



    elif belong == "metadata":
        apilists = Case.objects.filter(belong__contains="元数据管理平台接口")
    elif belong == "deposit_form":
        apilists = Case.objects.filter(belong__contains="续存记录接口")

    elif casename:
        apilists = Case.objects.filter(casename__contains=casename)
        print(apilists)
        if apilists.count() == 0:
            apilists = Case.objects.filter()
            L = []
            for weblist in apilists:
                if weblist.system == "erms" and "error" in weblist.result and "timestamp" in weblist.result:
                    # print("存在的啊")
                    data = {
                        "caseid": weblist.caseid,
                        "belong": weblist.belong,
                        "processid": weblist.isprocess,
                        "identity": weblist.identity,
                        "casename": weblist.casename,
                        "url": weblist.url,
                        "method": weblist.method,
                        "params": weblist.params,
                        "body": weblist.body,
                        "result": weblist.result
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


    L = []
    for weblist in apilists:
        if weblist.system == 'erms':
            data = {
                "caseid": weblist.caseid,
                "belong":weblist.belong,
                "processid":weblist.isprocess,
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


#transfer用例列表
@login_required
def transferlist_view(request):
    casename = request.GET.get("key[casename]","")
    if casename:
        print("搜索的用例名是:"+casename)
    belong = request.GET.get('belong',"")
    print("请求进入的模块是:"+belong)
    if casename == "" and belong == "":
        apilists = Case.objects.filter()
    elif belong == "user_yj":
        apilists = Case.objects.filter(belong__contains="用户模块接口")
    elif belong == "record_yj":
        apilists = Case.objects.filter(belong__contains="Record接口")
    elif belong == "resource_yj":
        apilists = Case.objects.filter(belong__contains="资源管理接口")
    elif belong == "yuwen_yj":
        apilists = Case.objects.filter(belong__contains="原文接口")
    elif belong == "navigation_yj":
        apilists = Case.objects.filter(belong__contains="导航接口")
    elif belong == "comments_yj":
        apilists = Case.objects.filter(belong__contains="意见接口")
    elif belong == "attribute_mapping_scheme_yj":
        apilists = Case.objects.filter(belong__contains="映射规则接口")
    elif belong == "volume_yj":
        apilists = Case.objects.filter(belong__contains="案卷相关接口")
    elif belong == "archives_yj":
        apilists = Case.objects.filter(belong__contains="档案相关接口")
    elif belong == "report_yj":
        apilists = Case.objects.filter(belong__contains="检测报告相关接口")
    elif belong == "transfer_form_yj":
        apilists = Case.objects.filter(belong__contains="移交表单相关接口")
    elif belong == "metadata_yj":
        apilists = Case.objects.filter(belong__contains="元数据平台接口")

    elif casename:
        apilists = Case.objects.filter(casename__contains=casename)
        print(apilists)
        if apilists.count() == 0:
            apilists = Case.objects.filter()
            L = []
            for weblist in apilists:
                if weblist.system == "transfer" and "error" in weblist.result and "timestamp" in weblist.result:
                    # print("存在的啊")
                    data = {
                        "caseid": weblist.caseid,
                        "belong": weblist.belong,
                        "processid": weblist.isprocess,
                        "identity": weblist.identity,
                        "casename": weblist.casename,
                        "url": weblist.url,
                        "method": weblist.method,
                        "params": weblist.params,
                        "body": weblist.body,
                        "result": weblist.result
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

    L = []
    for weblist in apilists:
        if weblist.system == "transfer":
            data = {
                "caseid": weblist.caseid,
                "belong":weblist.belong,
                "processid":weblist.isprocess,
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
@login_required
def create_apicase_views(request):
    if request.method == 'POST':
        casename = request.POST.get("casename", "")
        url = request.POST.get("url", "")
        method = request.POST.get("method", "")
        belong = request.POST.get("belong", "")
        params = request.POST.get("params", "")
        body = request.POST.get("body", "")
        identity = request.POST.get("identity", "")
        system = request.POST.get("system","")
        print(system)

        if system == "erms":
            try:
                Case.objects.create(casename=casename, identity=identity, url=url, system=system,
                                    method=method, params=params, body=body, belong=belong)
            except Exception as e:
                return HttpResponse(e)

        elif system == "transfer":
            try:
                Case.objects.create(casename=casename, identity=identity, url=url, system=system,
                                    method=method, params=params, body=body, belong=belong)
            except Exception as e:
                return HttpResponse(e)

        else:
            return HttpResponse("接口库没有此系统")

        return HttpResponse("操作成功")
    else:
        return HttpResponse("请求方式有误")


#删除api用例
@login_required
def delete_apicase_views(request):
    if request.method == "GET":
        ids = request.GET.get("ids","")
        if ids:
            print(ids)
            Case.objects.filter(caseid=ids).delete()
            return HttpResponse("操作成功")
        else:
            return HttpResponse("没有获取请求的ID")
    else:
        return HttpResponse("请求方式有误")


#更新api用例
@login_required
def update_apicase_views(request):
    if request.method == "GET":
        params = request.GET.get('params',"")
        body =request.GET.get("body","")
        ids = request.GET.get("ids","")
        if ids == "":
            return HttpResponse("没有获取请求的ID")
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
    else:
        caseid = request.POST.get("caseID","")
        if caseid == "":
            return HttpResponse("没有获取请求的ID")
        casename = request.POST.get("casename", "")
        url = request.POST.get("url", "")
        identity = request.POST.get("identity", "")
        method = request.POST.get("method", "")
        belong = request.POST.get("belong", "")
        params = request.POST.get("params", "")
        body = request.POST.get("body", "")
        system = request.POST.get('system',"")

        if "<" in body or ">" in body:
            print('存在需要替换的符号')
            a = body.replace("<", "＜")
            print(a)
            b = a.replace(">", "＞")
            print(b)
            Case.objects.filter(caseid=caseid).update(casename=casename, identity=identity, url=url,system=system,
                                  method=method, params=params, body=b, belong=belong)
        else:
            Case.objects.filter(caseid=caseid).update(casename=casename, identity=identity, url=url,system=system,
                                  method=method, params=params, body=body, belong=belong)
        if system == "erms":
            return HttpResponse("操作成功")
        else:
            return HttpResponse("操作成功")


#接口详情
@login_required
def detail_api_views(request):
    res = request.GET.get("id","")
    if res:
        id = Case.objects.get(caseid=res)
        identity = id.identity
        url =  id.url
        method = id.method
        params = id.params
        body = id.body
        casename = id.casename
        head = id.exceptres
        belong = id.belong
        result = id.result
        forward = str(int(res) + 1)
        print(forward)
        back = str(int(res) - 1)
        if identity == "sysadmin":
            identity = "系统管理员"
        if identity == "admin":
            identity = "单位管理员"
        if identity == "ast":
            identity = "单位档案员"
        if params == "":
            params = {
                "surprise":"params没有传参数哦!"
            }
            params = json.dumps(params, ensure_ascii=False, sort_keys=True, indent=2)
        if body == "":
            body = {
                "surprise": "body没有传参数哦!"
            }
            body = json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2)
        dic = {
            "identity": identity,
            "belong": belong,
            "casename": casename,
            "url": url,
            "method": method,
            "params": params,
            "body" : body,
            "result" : result,
            "head" : head,
            "forward" : forward,
            "back" : back
        }
        return render(request,"detail.html",{"dic":dic})
    else:
        return HttpResponse("没有传ID参数！")


#获取当前用户信息
@login_required
def get_userinfo_transfer_views(request):
    con = ConnDataBase()
    sysadmin = con.get_logininfo("yjadmin")
    a = request.GET.get("ids","")
    if a == "transfer":
        # admin = con.get_logininfo("admin")
        # ast = con.get_logininfo("ast")
        URL = str(con.get_logininfo("yjadmin")[2], 'utf-8')
        dic = {
            "系统管理员":{
                "账号":sysadmin[0],
                "密码":sysadmin[1],
                "令牌":sysadmin[3]
            },
            "访问路径":URL
        }
        dic1 = json.dumps(dic,ensure_ascii=False,sort_keys=True, indent=2)
        print(dic1)
        return HttpResponse(dic1)
    elif a == "erms":
        sysadmin = con.get_logininfo("sysadmin")
        admin = con.get_logininfo("admin")
        ast = con.get_logininfo("ast")
        URL = str(con.get_logininfo("sysadmin")[2], 'utf-8')
        dic = {
            "系统管理员": {
                "账号": sysadmin[0],
                "密码": sysadmin[1],
                "令牌": sysadmin[3]
            },
            "单位管理员": {
                "账号": admin[0],
                "密码": admin[1],
                "令牌": ast[3]
            },
            "单位档案员": {
                "账号": ast[0],
                "密码": ast[1],
                "令牌": ast[3]
            },
            "访问路径": URL
        }
        dic1 = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=2)
        print(dic1)
        return HttpResponse(dic1)
    else:
        return HttpResponse("没有你需要的信息")


#更改用户信息
@login_required
def update_userinfo_api_views(request):
    role = request.POST.get("identity","")
    print(role)
    username = request.POST.get("username","")
    print(username)
    password = request.POST.get("password","")
    print(password)
    try:
        con = ConnDataBase()
        con.update_logininfo(username,password,role)
        return HttpResponse("操作成功")
    except:
        return HttpResponse("链接数据库失败、修改用户信息失败")


#更改数据库存储的token
@login_required
def update_token_api_views(request):
    system = request.POST.get("system","")
    role = request.POST.get("identity", "")
    role1 = request.POST.get("identity1","")
    role2 = request.POST.get("identity2", "")
    role3 = request.POST.get("identity3", "")
    print(system)
    print(role3)
    if system == "erms":
        if role1 == "sysadmin":
            try:
                GetToken().get_token_by_role("sysadmin")
            except Exception as e:
                print(e)
                return HttpResponse("Failed to return "+ str(e))

        if role2 == "admin":
            try:
                GetToken().get_token_by_role("admin")
            except Exception as e:
                print(e)
                return HttpResponse("Failed to return "+ str(e))

        if role3 == "ast":
            try:
                GetToken().get_token_by_role("ast")
            except Exception as e:
                print(e)
                return HttpResponse("Failed to return "+ str(e))

        return HttpResponse("操作成功")

    elif system == "transfer":
        if role == "yjadmin":
            try:
                GetToken().get_token_by_role("yjadmin")
            except Exception as e:
                print(e)
                return HttpResponse("Failed to return "+ str(e))
        return HttpResponse("操作成功")


#执行用例
@login_required
def run_apicase_views(request):
    con = ConnDataBase()
    ids= request.GET.get("caseid").split(",")[:-1]
    print(ids)
    if len(ids) == 1:
        print("单一接口测试")
        d = {}
        for ucaseid in ids:
            id = Case.objects.get(caseid=ucaseid)
            #判断当前请求的系统，给对应的系统匹配上对应的URL
            if id.system == "erms":
                URL = str(con.get_logininfo("sysadmin")[2], 'utf-8')
            else:
                URL = str(con.get_logininfo("yjadmin")[2], 'utf-8')
            identity = id.identity
            Runmethod = RequestMethod(identity)
            url = URL + id.url
            # print(url)
            method = id.method
            params = id.params
            body = id.body
            casename = id.casename
            head = id.exceptres
            #eval()字符串转字典

            starttime = time.time()
            if body != "":
                if "＜" in body or "＞" in body:
                    print('body存在需要替换的符号')
                    a = body.replace("＜", "<")
                    b = a.replace("＞", ">")
                    body = b
                body = eval(body)
                if params:
                    params = eval(params)
                response = Runmethod.run_main(method, url, params, body)

            elif body == '':
                if params:
                    params = eval(params)
                response = Runmethod.run_main(method, url, params, body)

            endtime = time.time()
            runtime = round(endtime - starttime, 3)
            # 存为字典，转换为json格式
            print(response,"Ssssssssssssssssss")
            d[casename] = response
            if runtime > 0.5 and runtime <= 1.0:
                d[casename+"运行时间为"] = str(runtime)+"秒"
            elif runtime > 3.0:
                d[casename +"运行缓慢"] = str(runtime)+"秒"
            else:
                d[casename +"运行时间为"] = str(runtime)+"秒"
            d["＜"+ucaseid+"＞"+"负责人"] = head
            # print(d)
            # json格式化
            djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
            if "<" in djson or ">" in djson:
                print('result存在需要替换的符号')
                a = djson.replace("<", "＜")
                print(a)
                b = a.replace(">", "＞")
                print(b)
                Case.objects.filter(caseid=ucaseid).update(result=b)
            else:
                Case.objects.filter(caseid=ucaseid).update(result=djson)
            print(djson)
            # 发送钉钉消息
            # send_ding(djson)
            return HttpResponse(djson)

    else:
        #多个接口测试的情况
        print("多个接口测试")
        # 将每次运行的字典结果集用列表存储
        L = []
        for ucaseid in ids:
            # 每次循环创建一个字典，存储每次运行结束的接口，KEY以用例名字，Value以响应结果
            d = {}
            id = Case.objects.get(caseid=ucaseid)
            identity = id.identity
            if id.system == "erms":
                URL = str(con.get_logininfo("sysadmin")[2], 'utf-8')
            else:
                URL = str(con.get_logininfo("yjadmin")[2], 'utf-8')
            url = URL + id.url
            method = id.method
            params = id.params
            body = id.body
            casename = id.casename
            head = id.exceptres

            #c从数据库获取token
            Runmethod = RequestMethod(identity)

            # 计算运行前的时间
            starttime = time.time()
            if body != "":
                if "＜" in body or "＞" in body:
                    print('body存在需要替换的符号')
                    a = body.replace("＜", "<")
                    b = a.replace("＞", ">")
                    body = b
                body = eval(body)
                if params:
                    params = eval(params)
                response = Runmethod.run_main(method, url, params, body)

            elif body == '':
                if params:
                    params = eval(params)
                response = Runmethod.run_main(method, url, params, body)
            endtime = time.time()
            runtime = round(endtime - starttime, 3)
            print(runtime)

            d[casename] = response
            if runtime > 0.5 and runtime <= 1.0:
                d[casename + "运行时间为"] = str(runtime) + "秒"
            elif runtime > 3.0:
                d[casename + "运行缓慢"] = str(runtime) + "秒"
            else:
                d[casename + "运行时间为"] = str(runtime) + "秒"
            d["＜" + ucaseid + "＞" + "负责人"] = head

            # 将每个结果的字典存放在一个列表中
            L.append(d)
            # json格式化
            djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
            if "<" in djson or ">" in djson:
                print('result存在需要替换的符号')
                a = djson.replace("<", "＜")
                b = a.replace(">", "＞")
                Case.objects.filter(caseid=ucaseid).update(result=b)
            else:
                # 每次运行结束将每个接口返回的数据JOSN格式化存入数据库
                Case.objects.filter(caseid=ucaseid).update(result=djson)
            # print(L)
            # 创建一个字典存储包含所有字典的列表
        dict = {}
        dict["流程接口响应结果"] = L
        # 转换为JSON格式，且格式化
        djson_new = json.dumps(dict, ensure_ascii=False, sort_keys=True, indent=2)
        print(djson_new)
        # 发送钉钉消息
        # send_ding(djson_new)
        # 将JSON数据返回给前端
        return HttpResponse(djson_new)


#导出数据
@login_required
def export_data_views(request):
    System = request.GET.get("system","")
    Content = request.GET.get("content","")
    print(System,Content)
    list_obj = Case.objects.filter(system=System)
    if list_obj:
        # 创建工作薄
        ws = Workbook(encoding='utf-8')
        w = ws.add_sheet("错误接口")
        w.write(0, 0, "id")
        w.write(0, 1, "用例名称")
        w.write(0, 2, "请求地址")
        w.write(0, 3, "请求方式")
        w.write(0, 4, "params")
        w.write(0, 5, "body")
        w.write(0, 6, "结果")
        # 写入数据
        excel_row = 1
        if Content == "errorData":
            for obj in list_obj:
                if  "error" in obj.result and "timestamp" in obj.result:
                    data_id = obj.caseid
                    data_name = obj.casename
                    data_url = obj.url
                    data_method = obj.method
                    dada_params= obj.params
                    data_body = obj.body
                    data_result = obj.result
                    w.write(excel_row, 0, data_id)
                    w.write(excel_row, 1, data_name)
                    w.write(excel_row, 2, data_url)
                    w.write(excel_row, 3, data_method)
                    w.write(excel_row, 4, dada_params)
                    w.write(excel_row, 5, data_body)
                    w.write(excel_row, 6, data_result)
                    excel_row += 1
        elif Content == "allData":
            for obj in list_obj:
                data_id = obj.caseid
                data_name = obj.casename
                data_url = obj.url
                data_method = obj.method
                dada_params= obj.params
                data_body = obj.body
                data_result = obj.result
                w.write(excel_row, 0, data_id)
                w.write(excel_row, 1, data_name)
                w.write(excel_row, 2, data_url)
                w.write(excel_row, 3, data_method)
                w.write(excel_row, 4, dada_params)
                w.write(excel_row, 5, data_body)
                w.write(excel_row, 6, data_result)
                excel_row += 1
        # 检测文件是够存在
        # 方框中代码是保存本地文件使用，如不需要请删除该代码
        ###########################
        exist_file = os.path.exists("/Users/zhuzhanhao/Desktop/error_report.xls")
        if exist_file:
            os.remove(r"/Users/zhuzhanhao/Desktop/error_report.xls")
        ws.save("/Users/zhuzhanhao/Desktop/error_report.xls")
        ############################
        # sio = StringIO.StringIO()
        # BytesIO操作的数据类型为bytes
        sio = io.BytesIO()
        print(sio)
        ws.save(sio)
        sio.seek(0)
        response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
        print(response)
        response['Content-Disposition'] = 'attachment; filename=error_report.xls'
        response.write(sio.getvalue())#返回对象s中的所有数据
        print(response)
        return HttpResponse("操作成功")


#钉钉通知
def ding_ding_view(request):
    ids = request.GET.get("caseid","").split(",")[:-1]
    print(ids)
    if ids:
        for id in ids:
            caseid = Case.objects.get(caseid=id)
            if caseid:
                casename = caseid.casename
                head = caseid.exceptres
                result = caseid.result
                error_content = json.loads(result)[casename]["message"]
                dic = {casename:error_content}
                dic_json = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=2)
                send_ding(dic_json,head)
        return HttpResponse("操作成功")
    else:
        return HttpResponse("操作失败")