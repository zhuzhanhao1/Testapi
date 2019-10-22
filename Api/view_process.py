import os, sys, io

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import time
import json

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
# from Api.webuitest.DingDing import send_ding,send_image,send_link

currentUrl = os.path.dirname(__file__)
# 父文件路径
cur_path = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(cur_path)
from webuitest.conn_database import ConnDataBase


# 接口api用例首页
@login_required
def process_interface_view(request):
    # id = request.session.get('id')
    # uname = User.objects.get(id=id).uname
    a = request.GET.get("belong", "")
    case_count = Processapi.objects.all().count()
    return render(request, "process_interface.html", {"user": "朱占豪", "abq": a, "case_count": case_count})


# 用例列表
@login_required
def processlist_view(request):
    casename = request.GET.get("key[casename]", "")
    if casename:
        print("搜索的用例名是:" + casename)
    belong = request.GET.get('belong', "")
    print("请求进入的模块是:" + belong)
    if casename == "" and belong == "":
        apilists = Processapi.objects.filter().order_by("sortid")

    # 流程接口
    if belong:
        if belong == "unit":
            apilists = Processapi.objects.filter(belong="单位接口").order_by("sortid")
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

    # 按用例名称查询
    elif casename:
        apilists = Processapi.objects.filter(casename__contains=casename)
        print(apilists)
        if apilists.count() == 0:
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
                        "head":weblist.header
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
            "head": weblist.header
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

        all = Processapi.objects.filter()
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


# 导出数据
@login_required
def export_data_process_views(request):
    System = request.GET.get("system", "")
    Content = request.GET.get("content", "")
    print(System, Content)
    list_obj = Processapi.objects.filter(system=System)
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
                if "error" in obj.result and "timestamp" in obj.result:
                    data_id = obj.caseid
                    data_name = obj.casename
                    data_url = obj.url
                    data_method = obj.method
                    dada_params = obj.params
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
                dada_params = obj.params
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
        response.write(sio.getvalue())  # 返回对象s中的所有数据
        print(response)
        return HttpResponse("操作成功")


# 执行用例
@login_required
def run_processcase_view(request):
    con = ConnDataBase()
    URL = str(con.get_logininfo("sysadmin")[2], 'utf-8')
    ids = request.GET.get("caseid").split(",")[:-1]
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
        d[casename] = response
        d[casename + "运行时间为"] = str(runtime) + "秒"
        # d["＜" + ucaseid + "＞" + "负责人"] = head
        print(d)
        # json格式化
        djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
        if "<" in djson or ">" in djson:
            print('result存在需要替换的符号')
            a = djson.replace("<", "＜")
            print(a)
            b = a.replace(">", "＞")
            print(b)
            Processapi.objects.filter(caseid=ucaseid).update(result=b)
        else:
            Processapi.objects.filter(caseid=ucaseid).update(result=djson)
        print(djson)
        # 发送钉钉消息
        # send_ding(djson)
        return HttpResponse(djson)

    # 多个接口测试的情况
    else:
        print("多个接口测试")
        # 将每次运行的字典结果集用列表存储
        L = []
        for ucaseid in ids:
            # 每次循环创建一个字典，存储每次运行结束的接口，KEY以用例名字，Value以响应结果
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

            # 判断是否为流程测试接口，如果是的话先通过依赖数据的ID查询结果
            if isprocess == "True":
                print("我需要依赖别的接口哦！！！")
                dependid = Processapi.objects.get(caseid=depend_id)

                # 处理
                if "," in depend_key:
                    # 存在多个key时需要拆分字符串，通过循环赋值给每个结果
                    transfer_key = depend_key.split(",")
                    print(transfer_key)
                    l = []
                    for key in transfer_key:
                        if key:
                            l.append(key)

                    need_key = replace_key.split(",")
                    print(need_key)

                    b = 0
                    for i in l:
                        # 依赖的数据
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

                # 处理保管期限的列表接口返回的值
                elif "/" in depend_key:
                    # 存在多个key时需要拆分字符串，通过循环赋值给每个结果
                    transfer_key = depend_key.split("/")
                    print(transfer_key)
                    need_key = replace_key.split(",")
                    print(need_key)

                    # 依赖的数据
                    try:
                        depend_res = json.loads(dependid.result)[dependid.casename][(transfer_key[0])][0][
                            (transfer_key[1])]
                        print(depend_res)
                        if replace_position == "body":
                            if "＜" in body or "＞" in body:
                                print('body存在需要替换的符号')
                                a = body.replace("＜", "<")
                                b = a.replace("＞", ">")
                                body = b
                            body = eval(body)
                            body[(need_key[0])] = depend_res
                        elif replace_position == "params":
                            params = eval(params)
                            params[(need_key[0])] = depend_res

                        print("更新后的body:" + str(body))
                        print("更新后的params:" + str(params))
                        if params:
                            if type(params) == str:
                                params = eval(params)
                        if body:
                            if type(body) == str:
                                body = eval(body)
                        starttime = time.time()
                        response = Runmethod.run_main(method, url, params, body)

                    except:
                        print('请查看日志')


                # 处理访问控制策略的列表接口返回的值
                elif "-" in depend_key:
                    # 存在多个key时需要拆分字符串，通过循环赋值给每个结果
                    transfer_key = depend_key.split("-")
                    print(transfer_key)
                    need_key = replace_key.split(",")
                    print(need_key)

                    # 依赖的数据
                    print("我是body" + body)
                    for i in range(len(need_key)):
                        depend_res = json.loads(dependid.result)[dependid.casename][(transfer_key[0])][
                            (transfer_key[i + 1])]
                        print(depend_res)
                        if replace_position == "body":
                            if type(body) == str:
                                body = eval(body)
                            body[(need_key[i])] = depend_res
                        elif replace_position == "params":
                            if type(body) == str:
                                params = eval(params)
                            params[(need_key[i])] = depend_res

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


            # 不需要别的接口
            elif isprocess != "True":
                print("我不需要依赖别的接口！！！")
                # 计算运行前的时间
                starttime = time.time()
                if body != "":
                    if "＜" in body or "＞" in body:
                        print('noprocess-body存在需要替换的符号')
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
                Processapi.objects.filter(caseid=ucaseid).update(result=b)
            else:
                # 每次运行结束将每个接口返回的数据JOSN格式化存入数据库
                Processapi.objects.filter(caseid=ucaseid).update(result=djson)
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


def run_processcase_views(request):
    content = request.POST.get("request", "")
    content = json.loads(content)
    if len(content) == 1:
        identity = content[0].get("identity", "")  # 用户身份
        Runmethod = RequestMethod(identity)  # 根据用户身份获取请求头Token数据
        url = content[0].get("url", "")  # 登录地址
        casename = content[0].get("casename", "")  # 接口名
        method = content[0].get("method", "")  # 请求方式
        params = content[0].get("params", "")  # query数据
        body = content[0].get("body", "")  # body数据
        isprocess = content[0].get("isprocess", "")  # 是否存在依赖
        depend_id = content[0].get("depend_id", "")  # 依赖的ID
        depend_key = content[0].get("depend_key", "")  # 依=依赖的key
        replace_key = content[0].get("replace_key", "")  # 替换的key
        replace_position = content[0].get("replace_position", "")  # 替换的位置
        if isprocess == "True":
            return JsonResponse({"status_code": 500, "msg": "我是流程接口，请选择我和我依赖的ID一起运行!!!"})

        # 获取开始运行的时间
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
            if runtime > 0.5 and runtime <= 3.0:
                d["A.响应时长"] = str(runtime) + "秒"
            elif runtime > 3.0:
                d["B.响应时长"] = str(runtime) + "秒"
            else:
                d["S.响应时长"] = str(runtime) + "秒"
            # json格式化
            djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
            if "<" in djson or ">" in djson:
                print('result存在需要替换的符号')
                a = djson.replace("<", "＜")
                b = a.replace(">", "＞")
                Processapi.objects.filter(caseid=content[0]["caseid"]).update(result=b)
            else:
                Processapi.objects.filter(caseid=content[0]["caseid"]).update(result=djson)
            print(djson)
            return HttpResponse(djson)
        # 异常捕获
        except TypeError as e:
            print(e)
            return JsonResponse({"status_code": 500, "msg": "操作或函数应用于不适当类型的对象"})
        except json.decoder.JSONDecodeError as e:
            print(e)
            return JsonResponse({"status_code": 500, "msg": "json.loads()读取字符串报错"})

    else:
        # 多个接口测试的情况
        print("多个接口测试")
        # 将每次运行的字典结果集用列表存储ii
        L = []
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
            depend_id = i.get("depend_id", "")  # 接口名
            depend_key = i.get("depend_key", "")  # 接口名
            replace_key = i.get("replace_key", "")  # 接口名
            replace_position = i.get("replace_position", "")  # 接口名
            starttime = time.time()
            # 判断是否为流程测试接口，如果是的话先通过依赖数据的ID查询结果
            if isprocess == "True":
                print("我需要依赖别的接口哦！！！")
                dependid = Processapi.objects.get(caseid=depend_id)

                # 处理
                if "," in depend_key:
                    # 存在多个key时需要拆分字符串，通过循环赋值给每个结果
                    transfer_key = depend_key.split(",")
                    print(transfer_key)
                    l = []
                    for key in transfer_key:
                        if key:
                            l.append(key)
                    need_key = replace_key.split(",")
                    print(need_key)

                    b = 0
                    for i in l:
                        # 依赖的数据
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
                    print(body)
                    print(params)
                    response = Runmethod.run_main(method, url, json.dumps(params), json.dumps(body))

                # 处理保管期限的列表接口返回的值
                elif "/" in depend_key:
                    # 存在多个key时需要拆分字符串，通过循环赋值给每个结果
                    transfer_key = depend_key.split("/")
                    print(transfer_key)
                    need_key = replace_key.split(",")
                    print(need_key)

                    # 依赖的数据
                    try:
                        depend_res = json.loads(dependid.result)[dependid.casename][(transfer_key[0])][0][
                            (transfer_key[1])]
                        print(depend_res)
                        if replace_position == "body":
                            if "＜" in body or "＞" in body:
                                print('body存在需要替换的符号')
                                a = body.replace("＜", "<")
                                b = a.replace("＞", ">")
                                body = b
                            body = eval(body)
                            body[(need_key[0])] = depend_res
                        elif replace_position == "params":
                            params = eval(params)
                            params[(need_key[0])] = depend_res

                        print("更新后的body:" + str(body))
                        print("更新后的params:" + str(params))
                        if params:
                            if type(params) == str:
                                params = eval(params)
                        if body:
                            if type(body) == str:
                                body = eval(body)
                        response = Runmethod.run_main(method, url, params, body)

                    except:
                        print('请查看日志')


                # 处理访问控制策略的列表接口返回的值
                elif "-" in depend_key:
                    # 存在多个key时需要拆分字符串，通过循环赋值给每个结果
                    transfer_key = depend_key.split("-")
                    print(transfer_key)
                    need_key = replace_key.split(",")
                    print(need_key)

                    # 依赖的数据
                    print("我是body" + body)
                    for i in range(len(need_key)):
                        depend_res = json.loads(dependid.result)[dependid.casename][(transfer_key[0])][
                            (transfer_key[i + 1])]
                        print(depend_res)
                        if replace_position == "body":
                            if type(body) == str:
                                body = eval(body)
                            body[(need_key[i])] = depend_res
                        elif replace_position == "params":
                            if type(body) == str:
                                params = eval(params)
                            params[(need_key[i])] = depend_res

                    print("更新后的:" + str(body))
                    print("更新后的:" + str(params))
                    if params:
                        if type(params) == str:
                            params = eval(params)
                    if body:
                        if type(body) == str:
                            body = eval(body)
                    response = Runmethod.run_main(method, url, params, body)


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
                    print(response)
                    # 异常捕获
                except TypeError as e:
                    print(e)
                    return JsonResponse({"status_code": 500, "msg": "操作或函数应用于不适当类型的对象"})
                except json.decoder.JSONDecodeError as e:
                    print(e)
                    return JsonResponse({"status_code": 500, "msg": "json.loads()读取字符串报错"})
                # 获取运行完的时间
            endtime = time.time()
            runtime = round(endtime - starttime, 3)
            # 存为字典，转换为json格式
            d = {}
            d[casename] = response
            if runtime > 0.5 and runtime <= 3.0:
                d["A.响应时长"] = str(runtime) + "秒"
            elif runtime > 3.0:
                d["B.响应时长"] = str(runtime) + "秒"
            else:
                d["S.响应时长"] = str(runtime) + "秒"
            L.append(d)
            # json格式化
            djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
            if "<" in djson or ">" in djson:
                print('result存在需要替换的符号')
                a = djson.replace("<", "＜")
                b = a.replace(">", "＞")
                Processapi.objects.filter(caseid=caseid).update(result=b)
            else:
                Processapi.objects.filter(caseid=caseid).update(result=djson)

        dict = {}
        dict["流程接口响应结果"] = L
        # 转换为JSON格式，且格式化
        djson_new = json.dumps(dict, ensure_ascii=False, sort_keys=True, indent=2)
        print(djson_new)
        # 发送钉钉消息
        # send_ding(djson_new)
        # 将JSON数据返回给前端
        return HttpResponse(djson_new)




# 用例详情
@login_required
def detail_views(request):
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
            "surprise": "params没有传参数哦!"
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
        "body": body,
        "result": result,
        "head": head,
        "forward": forward,
        "back": back
    }
    return render(request, "detail.html", {"dic": dic})


# 定时任务
@login_required
def timetask_views(request):
    # 获取开始运行的时间
    start_time = request.POST.get("date", "")
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
    con = ConnDataBase()
    URL = str(con.get_logininfo("sysadmin")[2], 'utf-8')
    sched = BackgroundScheduler()
    # sched.add_job(job_function, args=(ids,), start_date=start_time, end_date=end_time, trigger=IntervalTrigger(seconds=interval_time_sjc))
    sched.add_job(job_function, "interval",seconds = interval_time_sjc,args=(ids,end_time,URL,sched))
    sched.start()
    # send_ding("定时任务开始,错误的消息才会@各位")
    return HttpResponse("定时任务在后台已经开始")


#定时任务job
def job_function(ids,end_time,URL,sched):
    locals_time= datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')[11:]
    locals_time_l = locals_time.split(":")
    locals_time_sjc = int(locals_time_l[0]) * 60 * 60 + int(locals_time_l[1]) * 60 + int(locals_time_l[2])
    print("现在时间:"+str(locals_time_sjc)+"-------"+"结束时间:"+str(end_time))
    if locals_time_sjc <= end_time:
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
            d[casename] = response
            d[casename + "运行时间为"] = str(runtime) + "秒"
            d["＜" + ucaseid + "＞" + "负责人"] = head
            print(d)
            # json格式化
            djson = json.dumps(d, ensure_ascii=False, sort_keys=True, indent=2)
            # send_ding(djson,head)
            if "<" in djson or ">" in djson:
                print('result存在需要替换的符号')
                a = djson.replace("<", "＜")
                print(a)
                b = a.replace(">", "＞")
                print(b)
                Processapi.objects.filter(caseid=ucaseid).update(result=b)
            else:
                Processapi.objects.filter(caseid=ucaseid).update(result=djson)
            print(djson)
            # 发送钉钉消息
            # send_ding(djson)
            # return HttpResponse(djson)
        # 多个接口测试的情况
        else:
            print("多个接口测试")
            # 将每次运行的字典结果集用列表存储
            L = []
            for ucaseid in ids:
                # 每次循环创建一个字典，存储每次运行结束的接口，KEY以用例名字，Value以响应结果
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

                # send_ding(casename + "开始执行。。。负责人:"+head)
                Runmethod = RequestMethod(identity)

                # 判断是否为流程测试接口，如果是的话先通过依赖数据的ID查询结果
                if isprocess == "True":
                    print("我需要依赖别的接口哦！！！")
                    dependid = Processapi.objects.get(caseid=depend_id)

                    # 处理
                    if "," in depend_key:
                        # 存在多个key时需要拆分字符串，通过循环赋值给每个结果
                        transfer_key = depend_key.split(",")
                        print(transfer_key)
                        l = []
                        for key in transfer_key:
                            if key:
                                l.append(key)

                        need_key = replace_key.split(",")
                        print(need_key)
                        b = 0
                        for i in l:
                            # 依赖的数据
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

                    # 处理保管期限的列表接口返回的值
                    elif "/" in depend_key:
                        # 存在多个key时需要拆分字符串，通过循环赋值给每个结果
                        transfer_key = depend_key.split("/")
                        print(transfer_key)
                        need_key = replace_key.split(",")
                        print(need_key)

                        # 依赖的数据
                        try:
                            depend_res = json.loads(dependid.result)[dependid.casename][(transfer_key[0])][0][
                                (transfer_key[1])]
                            print(depend_res)
                            if replace_position == "body":
                                if "＜" in body or "＞" in body:
                                    print('body存在需要替换的符号')
                                    a = body.replace("＜", "<")
                                    b = a.replace("＞", ">")
                                    body = b
                                body = eval(body)
                                body[(need_key[0])] = depend_res
                            elif replace_position == "params":
                                params = eval(params)
                                params[(need_key[0])] = depend_res

                            print("更新后的body:" + str(body))
                            print("更新后的params:" + str(params))
                            if params:
                                if type(params) == str:
                                    params = eval(params)
                            if body:
                                if type(body) == str:
                                    body = eval(body)
                            starttime = time.time()
                            response = Runmethod.run_main(method, url, params, body)

                        except:
                            print('请查看日志')


                    # 处理访问控制策略的列表接口返回的值
                    elif "-" in depend_key:
                        # 存在多个key时需要拆分字符串，通过循环赋值给每个结果
                        transfer_key = depend_key.split("-")
                        print(transfer_key)
                        need_key = replace_key.split(",")
                        print(need_key)

                        # 依赖的数据
                        print("我是body" + body)
                        for i in range(len(need_key)):
                            depend_res = json.loads(dependid.result)[dependid.casename][(transfer_key[0])][
                                (transfer_key[i + 1])]
                            print(depend_res)
                            if replace_position == "body":
                                if type(body) == str:
                                    body = eval(body)
                                body[(need_key[i])] = depend_res
                            elif replace_position == "params":
                                if type(body) == str:
                                    params = eval(params)
                                params[(need_key[i])] = depend_res

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
                # 不需要别的接口
                elif isprocess != "True":
                    print("我不需要依赖别的接口！！！")
                    # 计算运行前的时间
                    starttime = time.time()
                    if body != "":
                        if "＜" in body or "＞" in body:
                            print('noprocess-body存在需要替换的符号')
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
                if "error" in djson or "timestamp" in djson:
                    send_ding(djson,head)
                if "<" in djson or ">" in djson:
                    print('result存在需要替换的符号')
                    a = djson.replace("<", "＜")
                    b = a.replace(">", "＞")
                    Processapi.objects.filter(caseid=ucaseid).update(result=b)
                else:
                    # 每次运行结束将每个接口返回的数据JOSN格式化存入数据库
                    Processapi.objects.filter(caseid=ucaseid).update(result=djson)
                # print(L)
                # 创建一个字典存储包含所有字典的列表
            dict = {}
            dict["流程接口响应结果"] = L
            # 转换为JSON格式，且格式化
            djson_new = json.dumps(dict, ensure_ascii=False, sort_keys=True, indent=2)
            print(djson_new)
            if "error" not in djson_new or not "timestamp" in djson_new:
                pass
                # send_image()


            # 发送钉钉消息
            # send_ding(djson_new)
            # 将JSON数据返回给前端
            # return HttpResponse(djson_new)
    else:
        try:
            sched.shutdown()
        except RuntimeError:
            # send_ding("定时任务结束")
            pass


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
        if system == "erms":
            all = Processapi.objects.filter(Q(belong=belong) & Q(system="erms"))
        elif system == "transfer":
            all = Processapi.objects.filter(Q(belong=belong) & Q(system="transfer"))
        l = []
        for i in all:
            l.append(i.sortid)
        l.sort()
        flag = 0
        for d in datas:
            Processapi.objects.filter(caseid=d).update(sortid=l[flag])
            flag += 1
        return HttpResponse("排序成功")
