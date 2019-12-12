import io
import threading
import xlrd
from xlwt import *
import os,sys
import time
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from Api.common.run_method import RequestMethod
from Api.common.run_mehod_quick import RequestMethodQuick
from Api.common.get_header import  GetToken
from common.ding_ding import send_process_link,send_api_link
from Api.models import *


currentUrl = os.path.dirname(__file__)
#父文件路径
cur_path = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(cur_path)
from common.conn_database import ConnDataBase

num_progress = 0 # 全局变量进度数
thread_dict = {}

#接口测试首页
@login_required
def apiindex_view(request):
    a = request.GET.get("belong","")
    b = request.GET.get("system","")
    if b :
        case_count = Case.objects.filter(system=b).count()
    else:
        case_count =  Case.objects.filter().count()
    return render(request, "apiindex.html", {"user": "朱占豪", "abq":a, "case_count":case_count, "system":b})



#接口列表列表
def apilist_view(request):
    casename = request.GET.get("key[casename]","")
    filterSos = request.GET.get("filterSos","")
    belong = request.GET.get('belong',"")
    system = request.GET.get("system","")

    # 我是右下角搜索输入值运行的
    if filterSos:
        if filterSos == "[]" and casename == "":
            apilists = Case.objects.filter(system=system)
        else:
            L = []
            for i in json.loads(filterSos):
                filterSos_res = i.get("value")
                print(filterSos_res)

                apilists = Case.objects.filter(Q(casename__contains=filterSos_res) & Q(system=system)).order_by("sortid")
                for weblist in apilists:
                    data = {
                        "caseid": weblist.caseid,
                        "belong": weblist.belong,
                        "processid": weblist.isprocess,
                        "identity": weblist.identity,
                        "casename": weblist.casename,
                        "url": weblist.url,
                        "head": weblist.exceptres,
                        "method": weblist.method,
                        "params": weblist.params,
                        "body": weblist.body,
                        "result": weblist.result,
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

    elif casename:
        apilist = Case.objects.filter(Q(casename__contains=casename) & Q(system=system))
        print(apilist)
        if apilist.count() == 0:
            apilists = Case.objects.filter(
                Q(result__contains="error") & Q(result__contains="message") & Q(system=system))
        else:
            apilists = apilist

    elif system:
        if system == "tdr":
            if casename == "" and belong == "" and filterSos== "":
                apilists = Case.objects.filter(system='tdr').order_by("sortid")
            #流程接口
            # elif belong == "process":
                #匹配流程字段的值不能等于空
                # apilists = Case.objects.filter(~Q(isprocess= ''))
            elif belong:
                if belong == "unit":
                    apilists = Case.objects.filter(Q(belong__contains="单位接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "dept":
                    apilists = Case.objects.filter(Q(belong__contains="部门管理接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "user":
                    apilists = Case.objects.filter(Q(belong__contains="用户管理接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "views":
                    apilists = Case.objects.filter(Q(belong__contains="视图管理接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "category":
                    apilists = Case.objects.filter(Q(belong__contains="门类管理接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "view":
                    apilists = Case.objects.filter(Q(belong__contains="视图自定义接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "record":
                    apilists = Case.objects.filter(Q(belong__contains="Record接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "document":
                    apilists = Case.objects.filter(Q(belong__contains="文档管理接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "volume":
                    apilists = Case.objects.filter(Q(belong__contains="案卷管理接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "archives":
                    apilists = Case.objects.filter(Q(belong__contains="档案管理接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "resource":
                    apilists = Case.objects.filter(Q(belong__contains="资源管理接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "navigation":
                    apilists = Case.objects.filter(Q(belong__contains="导航管理接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "common":
                    apilists = Case.objects.filter(Q(belong__contains="公共操作相关接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "common_folder":
                    apilists = Case.objects.filter(Q(belong__contains="通用文件夹管理接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "metadata":
                    apilists = Case.objects.filter(Q(belong__contains="元数据管理平台接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "attribute_mapping_scheme":
                    apilists = Case.objects.filter(Q(belong__contains="映射规则接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "appraisal_task":
                    apilists = Case.objects.filter(Q(belong__contains="鉴定任务接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "appraisal_archives":
                    apilists = Case.objects.filter(Q(belong__contains="鉴定档案接口") & Q(system="tdr")).order_by("sortid")

                elif belong == "warehouse":
                    apilists = Case.objects.filter(Q(belong__contains="库房接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "warehouse_address":
                    apilists = Case.objects.filter(Q(belong__contains="库房存址") & Q(system="tdr")).order_by("sortid")
                elif belong == "warehouseLayer":
                    apilists = Case.objects.filter(Q(belong__contains="库房层接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "subject":
                    apilists = Case.objects.filter(Q(belong__contains="专题接口") & Q(system="tdr")).order_by("sortid")

                elif belong == "subject_relation":
                    apilists = Case.objects.filter(Q(belong__contains="专题档案接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "usage_archives":
                    apilists = Case.objects.filter(Q(belong__contains="利用档案接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "usage":
                    apilists = Case.objects.filter(Q(belong__contains="档案利用接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "file_retrieval":
                    apilists = Case.objects.filter(Q(belong__contains="实体调卷管理接口") & Q(system="tdr")).order_by("sortid")
                elif belong == "retrieval_archives":
                    apilists = Case.objects.filter(Q(belong__contains="调卷单内档案详情") & Q(system="tdr")).order_by("sortid")


        elif system == "erms":
            if casename == "" and belong == "" and filterSos == "":
                apilists = Case.objects.filter(system='erms').order_by("sortid")
            # 流程接口
            # elif belong == "process":
            # 匹配流程字段的值不能等于空
            # apilists = Case.objects.filter(~Q(isprocess= ''))
            elif belong:
                if belong == "unit":
                    apilists = Case.objects.filter(Q(belong__contains="单位接口") & Q(system="erms")).order_by("sortid")
                elif belong == "dept":
                    apilists = Case.objects.filter(Q(belong__contains="部门管理接口") & Q(system="erms")).order_by("sortid")
                elif belong == "user":
                    apilists = Case.objects.filter(Q(belong__contains="用户管理接口") & Q(system="erms")).order_by("sortid")
                elif belong == "views":
                    apilists = Case.objects.filter(Q(belong__contains="视图管理接口") & Q(system="erms")).order_by("sortid")
                elif belong == "policy":
                    apilists = Case.objects.filter(Q(belong__contains="保留处置策略接口") & Q(system="erms")).order_by("sortid")
                elif belong == "role":
                    apilists = Case.objects.filter(Q(belong__contains="角色管理接口") & Q(system="erms")).order_by("sortid")
                elif belong == "data_form_config":
                    apilists = Case.objects.filter(Q(belong__contains="数据表单配置管理接口") & Q(system="erms")).order_by("sortid")
                elif belong == "category":
                    apilists = Case.objects.filter(Q(belong__contains="门类管理接口") & Q(system="erms")).order_by("sortid")
                elif belong == "class":
                    apilists = Case.objects.filter(Q(belong__contains="类目模块接口") & Q(system="erms")).order_by("sortid")
                elif belong == "acl":
                    apilists = Case.objects.filter(Q(belong__contains="访问控制权限接口") & Q(system="erms")).order_by("sortid")
                elif belong == "view":
                    apilists = Case.objects.filter(Q(belong__contains="视图自定义接口") & Q(system="erms")).order_by("sortid")
                elif belong == "record":
                    apilists = Case.objects.filter(Q(belong__contains="Record接口") & Q(system="erms")).order_by("sortid")
                elif belong == "document":
                    apilists = Case.objects.filter(Q(belong__contains="文档管理接口") & Q(system="erms")).order_by("sortid")
                elif belong == "volume":
                    apilists = Case.objects.filter(Q(belong__contains="案卷管理接口") & Q(system="erms")).order_by("sortid")
                elif belong == "archives":
                    apilists = Case.objects.filter(Q(belong__contains="档案管理接口") & Q(system="erms")).order_by("sortid")
                elif belong == "resource":
                    apilists = Case.objects.filter(Q(belong__contains="资源管理接口") & Q(system="erms")).order_by("sortid")
                elif belong == "navigation":
                    apilists = Case.objects.filter(Q(belong__contains="导航管理接口") & Q(system="erms")).order_by("sortid")
                elif belong == "data_form":
                    apilists = Case.objects.filter(Q(belong__contains="数据表单管理接口") & Q(system="erms")).order_by("sortid")
                elif belong == "file_plan":
                    apilists = Case.objects.filter(Q(belong__contains="文件计划管理接口") & Q(system="erms")).order_by("sortid")
                elif belong == "common":
                    apilists = Case.objects.filter(Q(belong__contains="公共操作相关接口") & Q(system="erms")).order_by("sortid")
                elif belong == "common_folder":
                    apilists = Case.objects.filter(Q(belong__contains="通用文件夹管理接口") & Q(system="erms")).order_by("sortid")
                elif belong == "metadata":
                    apilists = Case.objects.filter(Q(belong__contains="元数据管理平台接口") & Q(system="erms")).order_by("sortid")
                elif belong == "deposit_form":
                    apilists = Case.objects.filter(Q(belong__contains="续存记录接口") & Q(system="erms")).order_by("sortid")
                elif belong == "attribute_mapping_scheme":
                    apilists = Case.objects.filter(Q(belong__contains="映射规则接口") & Q(system="erms")).order_by("sortid")
                elif belong == "transfer_form":
                    apilists = Case.objects.filter(Q(belong__contains="移交表单信息接口") & Q(system="erms")).order_by("sortid")

        elif system == "transfer":
            if casename == "" and belong == "" and filterSos == "":
                apilists = Case.objects.filter(system='transfer')
            # 我是左侧的导航链接存在运行的
            elif belong:
                if belong == "user":
                    apilists = Case.objects.filter(Q(belong__contains="用户模块接口") & Q(system="transfer")).order_by("sortid")
                elif belong == "record":
                    apilists = Case.objects.filter(Q(belong__contains="Record接口") & Q(system="transfer")).order_by("sortid")
                elif belong == "resource":
                    apilists = Case.objects.filter(Q(belong__contains="资源管理接口") & Q(system="transfer")).order_by("sortid")
                elif belong == "document":
                    apilists = Case.objects.filter(Q(belong__contains="原文接口") & Q(system="transfer")).order_by("sortid")
                elif belong == "navigation":
                    apilists = Case.objects.filter(Q(belong__contains="导航接口") & Q(system="transfer")).order_by("sortid")
                elif belong == "comments":
                    apilists = Case.objects.filter(Q(belong__contains="意见接口") & Q(system="transfer")).order_by("sortid")
                elif belong == "attribute_mapping_scheme":
                    apilists = Case.objects.filter(Q(belong__contains="映射规则接口") & Q(system="transfer")).order_by("sortid")
                elif belong == "volume":
                    apilists = Case.objects.filter(Q(belong__contains="案卷相关接口") & Q(system="transfer")).order_by("sortid")
                elif belong == "archives":
                    apilists = Case.objects.filter(Q(belong__contains="档案相关接口") & Q(system="transfer")).order_by("sortid")
                elif belong == "report":
                    apilists = Case.objects.filter(Q(belong__contains="检测报告相关接口") & Q(system="transfer")).order_by("sortid")
                elif belong == "transfer_form":
                    apilists = Case.objects.filter(Q(belong__contains="移交表单相关接口") & Q(system="transfer")).order_by("sortid")
                elif belong == "metadata":
                    apilists = Case.objects.filter(Q(belong__contains="元数据平台接口") & Q(system="transfer")).order_by("sortid")

    else:
        apilists = Case.objects.filter().order_by("sortid")

    L = []
    for weblist in apilists:
        data = {
            "caseid": weblist.caseid,
            "belong": weblist.belong,
            "processid": weblist.isprocess,
            "identity": weblist.identity,
            "casename": weblist.casename,
            "url": weblist.url,
            "head": weblist.exceptres,
            "method": weblist.method,
            "params": weblist.params,
            "body": weblist.body,
            "result": weblist.result,
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


#创建api用例
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
        head = request.POST.get("head","")
        print(system)
        all = Case.objects.filter()
        L = []
        for i in all:
            L.append(i.sortid)
        m = max(L) + 1
        if system:
            try:
                Case.objects.create(casename=casename, identity=identity, url=url, system=system,duration=1,
                                    method=method, params=params, body=body, belong=belong,sortid=m,exceptres=head)
            except Exception as e:
                return HttpResponse(e)

        else:
            return HttpResponse("接口库没有此系统")

        return HttpResponse("操作成功")
    else:
        return HttpResponse("请求方式有误")

#更新api用例
@login_required
def update_apicase_views(request):
    if request.method == "GET":
        params = request.GET.get('params',"")
        body =request.GET.get("body","")
        head = request.GET.get("head","")
        ids = request.GET.get("ids","")
        if ids == "":
            return HttpResponse("没有获取请求的ID")
        print(ids)
        if params:
            print(params)
            if params == "1":
                Case.objects.filter(caseid=ids).update(params="")
            else:
                Case.objects.filter(caseid=ids).update(params=params)

        elif body:
            print(body)
            if body == "1":
                Case.objects.filter(caseid=ids).update(body="")
            elif "<" in body or ">" in body:
                print('存在需要替换的符号')
                a = body.replace("<", "＜")
                print(a)
                b = a.replace(">", "＞")
                print(b)
                Case.objects.filter(caseid=ids).update(body=b)
            else:
                Case.objects.filter(caseid=ids).update(body=body)

        elif head:
            Case.objects.filter(caseid=ids).update(exceptres=head)
        return HttpResponse("操作成功")
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
        head = request.POST.get("head","")

        if "<" in body or ">" in body:
            print('存在需要替换的符号')
            a = body.replace("<", "＜")
            print(a)
            b = a.replace(">", "＞")
            print(b)
            Case.objects.filter(caseid=caseid).update(casename=casename, identity=identity, url=url,system=system,
                                  method=method, params=params, body=b, belong=belong, exceptres=head)
        else:
            Case.objects.filter(caseid=caseid).update(casename=casename, identity=identity, url=url,system=system,
                                  method=method, params=params, body=body, belong=belong, exceptres=head)
        # if system == "erms":
        #     return HttpResponse("操作成功")
        # else:
        return HttpResponse("操作成功")

#删除api用例
@login_required
def delete_apicase_views(request):
    if request.method == "GET":
        ids = request.GET.get("ids","")
        id = request.GET.get("id", "")
        if ids:
            caseids = json.loads(ids)
            print(ids)
            for caseid in caseids:
                Case.objects.filter(caseid=caseid.get("caseid","")).delete()
            return HttpResponse("操作成功")
        elif id:
            Case.objects.filter(caseid=id).delete()
            return HttpResponse("操作成功")
        else:
            return HttpResponse("没有获取请求的ID")
    else:
        return HttpResponse("请求方式有误")

#接口详情
def get_apicase_details_views(request):
    res = request.GET.get("id","")
    if res:
        id = Case.objects.get(caseid=res)
        identity = id.identity
        url = "/".join(id.url.split("/")[-2:])
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
            "body" : body,
            "result" : result,
            "head" : head
        }
        return render(request, "detail.html", {"dic":dic})
    else:
        return HttpResponse("没有传ID参数！")


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
        return HttpResponse("连接数据库失败、修改用户信息失败")


#更改数据库存储的token
@login_required
def update_token_api_views(request):
    system = request.POST.get("system","")
    sysadmin = request.POST.get("sysadmin", "")
    admin = request.POST.get("admin","")
    ast = request.POST.get("ast", "")
    transferadmin = request.POST.get("transferadmin", "")
    sjzjy = request.POST.get("sjzjy", "")
    sjshy = request.POST.get("sjshy", "")
    tdradmin = request.POST.get("tdradmin", "")

    try:
        if system == "erms":
            if sysadmin == "sysadmin":
                GetToken("sysadmin").get_token_by_role("sysadmin")
            if admin == "admin":
                GetToken("admin").get_token_by_role("admin")
            if ast == "ast":
                 GetToken("ast").get_token_by_role("ast")
            else:
                return HttpResponse("请先选择一个角色去获取AccessToken")

        elif system == "transfer":
            if transferadmin == "transferadmin":
                GetToken("transferadmin").get_token_by_role("transferadmin")
            if sjzjy == "sjzjy":
                GetToken("sjzjy").get_token_by_role("sjzjy")
            if sjshy == "sjshy":
                GetToken("sjshy").get_token_by_role("sjshy")
            else:
                return HttpResponse("请先选择一个角色去获取AccessToken")

        elif system == "tdr":
            if tdradmin == "tdradmin":
                GetToken("tdradmin").get_token_by_role("tdradmin")
            else:
                return HttpResponse("请先选择一个角色去获取AccessToken")

    except Exception as e:
        print(e)
        return HttpResponse("Failed to return Token")


    return HttpResponse("操作成功")


#执行用例
@login_required
def run_apicase_views(request):
    content = request.POST.get("request","")
    content = json.loads(content)
    if len(content) == 1:
        identity = content[0].get("identity","")  #用户身份
        Runmethod = RequestMethod(identity) #根据用户身份获取请求头Token数据
        url = content[0].get("url","")     #登录地址
        method = content[0].get("method","")     #请求方式
        params = content[0].get("params","")      #query数据
        body = content[0].get("body","")         #body数据
        casename = content[0].get("casename","")  #接口名

        #获取开始运行的时间
        starttime = time.time()
        if "＜" in body or "＞" in body:
            print('body存在需要替换的符号')
            a = body.replace("＜", "<")
            b = a.replace("＞", ">")
            body = b
        try:
            response = Runmethod.run_main(method, url, params, body)
            print(response)
            # 获取运行完的时间
            endtime = time.time()
            runtime = round(endtime - starttime, 3)
            # 存为字典，转换为json格式
            d = {}
            d[casename] = response
            # json格式化
            djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
            if "<" in djson or ">" in djson:
                print('result存在需要替换的符号')
                a = djson.replace("<", "＜")
                b = a.replace(">", "＞")
                Case.objects.filter(caseid=content[0]["caseid"]).update(result=b)
            else:
                Case.objects.filter(caseid=content[0]["caseid"]).update(result=djson)
            Case.objects.filter(caseid=content[0]["caseid"]).update(duration=runtime)
            print(djson)
            return HttpResponse(djson)
        #异常捕获
        except TypeError as e:
            print(e)
            return JsonResponse({"status_code": 500, "msg": "操作或函数应用于不适当类型的对象"})
        except json.decoder.JSONDecodeError as e:
            print(e)
            return JsonResponse({"status_code": 500, "msg": "json.loads()读取字符串报错"})

    else:
        #多个接口测试的情况
        print("多个接口测试")
        # 将每次运行的字典结果集用列表存储ii
        L = []
        for i in content:
            identity = i.get("identity", "")  # 用户身份
            Runmethod = RequestMethod(identity)  # 根据用户身份获取请求头Token数据
            url = i.get("url", "")  # 登录地址
            method = i.get("method", "")  # 请求方式
            params = i.get("params", "")  # query数据
            body = i.get("body", "")  # body数据
            casename = i.get("casename", "")  # 接口名

            starttime = time.time()
            if "＜" in body or "＞" in body:
                print('body存在需要替换的符号')
                a = body.replace("＜", "<")
                b = a.replace("＞", ">")
                body = b
            try:
                response = Runmethod.run_main(method, url, params, body)
                print(response)
                # 获取运行完的时间
                endtime = time.time()
                runtime = round(endtime - starttime, 3)
                # 存为字典，转换为json格式
                d = {}
                d[casename] = response
                L.append(d)
                # json格式化
                djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
                if "<" in djson or ">" in djson:
                    print('result存在需要替换的符号')
                    a = djson.replace("<", "＜")
                    b = a.replace(">", "＞")
                    Case.objects.filter(caseid=i["caseid"]).update(result=b)
                else:
                    Case.objects.filter(caseid=i["caseid"]).update(result=djson)
                Case.objects.filter(caseid=i["caseid"]).update(duration=runtime)
            #异常捕获
            except TypeError as e:
                print(e)
                return JsonResponse({"status_code": 500, "msg": "操作或函数应用于不适当类型的对象"})
            except json.decoder.JSONDecodeError as e:
                print(e)
                return JsonResponse({"status_code": 500, "msg": "json.loads()读取字符串报错"})
        dict = {}
        dict["流程接口响应结果"] = L
        # 转换为JSON格式，且格式化
        djson_new = json.dumps(dict, ensure_ascii=False, sort_keys=True, indent=2)
        print(djson_new)
        # 将JSON数据返回给前端
        return HttpResponse(djson_new)



#导入用例
@login_required
def import_apicase_views(request):
    if request.method == 'POST':
        f = request.FILES.get('file')
        print(f)
        excel_type = f.name.split('.')[1]
        if excel_type in ['xlsx', 'xls']:
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            rows = table.nrows  # 总行数
            print(rows)
            try:
                with transaction.atomic():  # 控制数据库事务交易
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        print(rowVlaues)
                        # print(int(rowVlaues[0]))
                        # major = models.TMajor.objects.filter(majorid=rowVlaues[1]).first()
                        Case.objects.create(belong=rowVlaues[0],identity=rowVlaues[1],
                                               casename=rowVlaues[2],
                                               url=rowVlaues[3], method=rowVlaues[4],
                                               params=rowVlaues[5], body=rowVlaues[6],
                                               exceptres=rowVlaues[7],system=rowVlaues[8])
                        print('插入成功')
            except:
                print('解析excel文件或者数据插入错误')
                return HttpResponse("Failed!!!")
            return HttpResponse("ok success!请按浏览器的返回键返回，由于请求通过form表单中，html input 标签的“file”完成，没采用ajax请求。")
            # return JsonResponse({"status":200,"message":"导入数据成功"})
        else:
            print('上传文件类型错误！')
            return JsonResponse({"status": 200, "message": "导入数据失败"})


#钉钉通知
def ding_ding_view(request):
    ids = request.GET.get("caseid","").split(",")[:-1]
    isporcess = request.GET.get("isprocess","")
    for id in ids:
        print(id)
        if isporcess == "no":
            data = Case.objects.get(caseid=id)
            casename = data.casename
            send_api_link(id, casename + "-/详情-->")
        elif isporcess == "yes":
            data = Processapi.objects.get(caseid=id)
            casename = data.casename
            print(casename)
            send_process_link(id, casename + "-/详情-->")
        # head = data.exceptres
        # if data.result:
        #     res = json.loads(data.result)
        #     result = [res]
        # else:
        #     result = ""
        # if data.params:
        #     par = json.loads(data.params)
        #     params = [par]
        # else:
        #     params= ""
        # if data.body:
        #     bod = json.loads(data.body)
        #     body = [bod]
        # else:
        #     body=""
        # url = data.url
        # method = data.method
        # dic = {
        #     "InterfaceName":casename,
        #     "Url": url,
        #     "Method":method,
        #     "Query":params,
        #     "Body":body,
        #     "Response":result
        # }
        # dic_json = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=2)
        # print(dic_json)
        #
        # send_ding(dic_json,head)
    return HttpResponse("操作成功")


#请求接口参数详情
def field_apilist_views(request):
    id = request.GET.get("caseid","")
    print("详情查看的ID是:"+id)
    if id:
        L = []
        data = ConnDataBase()
        res = data.get_requestParams(int(id))
        for i in res:
            data = {
                "parameterName":i[0],
                "parameterThat": i[1],
                "requestType": i[2],
                "isMust":i[3],
                "dataType":i[4]
            }
            L.append(data)
            print(L)
        # pageindex = request.GET.get('page', "")
        # pagesize = request.GET.get("limit", "")
        # pageInator = Paginator(L, pagesize)
        # # 分页
        # contacts = pageInator.page(pageindex)
        # res = []
        # for contact in contacts:
        #     res.append(contact)
        datas = {"code": 0, "msg": "", "count": len(L), "data": L}
        return JsonResponse(datas)


#获取当前用户信息
@login_required
def get_userinfo_views(request):
    con = ConnDataBase()
    datas = con.get_logininfos()
    L = []
    for data in datas:
        dict = {
            "identity":data[2],
            "username":data[0],
            "password":data[1],
            "url":str(data[3],"utf-8"),
            "accessToken":data[4],
            "system":data[5],
            "role":data[6]
        }
        L.append(dict)
    res = {"code": 0, "msg": "", "count": len(L), "data": L}
    return JsonResponse(res)


#快速测试
@login_required
def quickTest_views(request):
    quickMethod = RequestMethodQuick()
    url = request.POST.get("addURL","")
    method = request.POST.get("Method","")
    headers = request.POST.get("addmergeheaders","")
    params = request.POST.get("addmergeformdatas","")
    body = request.POST.get("body","")
    print(url)
    print(method)
    print(headers)
    print(params)
    print(body)
    try:
        response = quickMethod.run_main(method,url,headers,params,body)
        response = json.dumps(response, ensure_ascii=False, sort_keys=True, indent=2)
        print(response)
        return HttpResponse(response)
    except TypeError as e:
        print(e)
        return JsonResponse({"status_code":500,"msg":"操作或函数应用于不适当类型的对象"})
    except json.decoder.JSONDecodeError as e:
        print(e)
        return JsonResponse({"status_code":500,"msg":"json.loads()读取字符串报错"})


#排序
@login_required
def web_sort_views(request):
    if request.method == "GET":
        oldIndex = int(request.GET.get("oldIndex",""))+1
        newIndex = int(request.GET.get("newIndex", ""))+1
        if oldIndex < newIndex:
            q = []
            for i in range(oldIndex,newIndex):
                a = i + 1
                for b in Case.objects.filter(sortid=a):
                    q.append(b.caseid)
                Case.objects.filter(sortid=a).update(sortid=i)
            l = Case.objects.filter(sortid=oldIndex)
            for lll in l:
                if lll.caseid not in q:
                    Case.objects.filter(caseid=lll.caseid).update(sortid=newIndex)
        elif oldIndex > newIndex:
            Case.objects.filter(sortid=oldIndex).update(sortid=-1)
            L = []
            for i in range(newIndex,oldIndex):
                L.append(i)
            e = L[::-1]
            for r in e:
                Case.objects.filter(sortid=r).update(sortid=r+1)
            Case.objects.filter(sortid=-1).update(sortid=newIndex)
        return HttpResponse("排序成功")
    else:
        data = request.POST.get("data","")
        belong = request.POST.get("belong","")
        system = request.POST.get("system", "")
        datas = json.loads(data)
        if system == "erms":
            all = Case.objects.filter(Q(belong=belong) & Q(system="erms"))
        elif system == "transfer":
            all = Case.objects.filter(Q(belong=belong) & Q(system="transfer"))
        elif system == "tdr":
            all = Case.objects.filter(Q(belong=belong) & Q(system="tdr"))
        l = []
        for i in all:
            l.append(i.sortid)
        l.sort()
        flag = 0
        for d in datas:
            Case.objects.filter(caseid=d).update(sortid=l[flag])
            flag += 1
        return HttpResponse("排序成功")


#进度条
@login_required
def show_api_views(request):
    global num_progress
    print('show_api----------'+str(num_progress))
    #当进度百分百的时候，需要吧全局变量初始化，以便下次请求的时候进度条是重0开始，否则默认都是百分之百了
    if num_progress == 100:
        num_progress = 0
        return JsonResponse(100, safe=False)
    #当进度不是百分之百的时候，返回当前进度
    else:
        return JsonResponse(num_progress, safe=False)


#多线程运行，单一接口测试仅支持一个接口的重复调用
def repeatrun_api_views(request):
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

#多线程的子方法
def run_apicase(start,end,content):
    global num_progress
    global thread_dict
    print(start)
    print(type(start))
    print(end)
    print(content)
    print(type(content))

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

                if runtime > 0 and runtime < 1.0:
                    d["S.响应时长"] = str(int(runtime * 1000)) + "毫秒"
                elif runtime >= 1.0 and runtime < 3.0:
                    d["A.响应时长"] = str(runtime) + "秒"
                elif runtime >= 3.0:
                    d["B.响应时长"] = str(runtime) + "秒"
                L.append(d)
                # json格式化
                djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
                print(djson)
                if "身份认证失败" in djson:
                    num_progress = 100
                    return JsonResponse({"status_code": 401, "msg": "身份认证失败。 'AccessKey' 或 'AccessToken' 不正确。"})
                if "<" in djson or ">" in djson:
                    print('result存在需要替换的符号')
                    a = djson.replace("<", "＜")
                    b = a.replace(">", "＞")
                    Case.objects.filter(caseid=caseid).update(result=b)
                else:
                    Case.objects.filter(caseid=caseid).update(result=djson)

            b = time.time()
            c = round(b - a, 3)
            thread_dict["接口自动化响应内容"] = L
            thread_dict["接口总消耗时间"] = c
            thread_dict["接口平均响应时间"] = c/end
            # 发送钉钉消息
            # send_ding(djson_new)
            return thread_dict

        except TypeError as e:
            print(e)
            # send_ding({"status_code": 500, "msg": "异常的id为:"+caseid+","+casename+"操作或函数应用于不适当类型的对象"})
            return {"status_code": 500, "msg": "异常的id为:"+caseid+","+casename+"操作或函数应用于不适当类型的对象"}
        except json.decoder.JSONDecodeError as e:
            print(e)
            # send_ding({"status_code": 500, "msg": "异常的id为:" + caseid + "," + casename + "json.loads()读取字符串报错"})
            return {"status_code": 500, "msg": "异常的id为:"+caseid+","+casename+"操作或函数应用于不适当类型的对象"}

    else:
        # 多个接口测试的情况
        print("多个接口测试")
        pass


#导出数据，暂时放弃使用，导出的数据量大会出错，使用前端的方案导出
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


#遍历修改字段，测试用
def zzh_test_views(request):
    all_case = Case.objects.filter()
    for case in all_case:
        URL = case.url.replace("\r","")
        Case.objects.filter(caseid=case.caseid).update(url=URL)
        print(case.caseid)
    return HttpResponse("success!")



#检索
def search_views(request):
    data = request.GET.get("key","")
    print(data)

    if data:
        apilist = Case.objects.filter(Q(casename__contains=data) | Q(url__contains=data) | Q(exceptres__contains=data))
    else:
        apilist = Case.objects.filter()
    L = []
    for weblist in apilist:
        data = {
            "caseid": weblist.caseid,
            "belong": weblist.belong,
            "processid": weblist.isprocess,
            "identity": weblist.identity,
            "casename": weblist.casename,
            "url": weblist.url,
            "head": weblist.exceptres,
            "method": weblist.method,
            "params": weblist.params,
            "body": weblist.body,
            "result": weblist.result,
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

