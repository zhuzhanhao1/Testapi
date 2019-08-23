import os

import xlrd
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.shortcuts import render
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import *
from Api.interfacetest.run_method import RequestMethod
from Api.interfacetest.get_header import ReqParam
import time
import json
from django.core import serializers
# Create your views here.

#注册用户
def registered_views(request):
    if request.method == 'GET':
        return render(request,'registered.html')
    else:
        # 接受提交的信息并注册回数据库
        upwd = request.POST['upwd']
        uname = request.POST['uname']
        uemail = request.POST['uemail']
        uphone = request.POST['uphone']
        # 验证手机号码是否已经存在
        uList = User.objects.filter(uphone=uphone)
        if uList:
            #断定手机号码是存在的　给出错误提示
            return render(request,'registered.html',{'error':'手机号码已经存在',
                                                'uname':uname,
                                                'uemail':uemail})
        dic = {
            'uphone':uphone,
            'upwd':upwd,
            'uname':uname,
            'uemail':uemail
        }
        User(**dic).save()
        return HttpResponse('注册成功')

#用户登录
def login_views(request):
    if request.method == 'POST':
        #实现登录操作
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']
        uList = User.objects.filter(uphone=uphone,upwd=upwd)
        #登录成功
        if uList:
            #从cookies中获取登入页面之前的url
            url = request.COOKIES.get('url','/')
            print(url)
            resp = HttpResponseRedirect(url)
            #从cookies中将url删除出去
            if 'url' in request.COOKIES:
                resp.delete_cookie('url')
            #将登录信息保存进session
            request.session['uphone'] = uphone
            request.session['id'] = uList[0].id
            #是否记住密码
            if 'isSaved' in request.POST:
                #将登录信息保存进cookie
                resp.set_cookie('id',uList[0].id,60*60*24*365)
                resp.set_cookie('uphone',uphone,60*60*24*365)
            # uname = User.objects.get(id=uList[0].id).uname
            # return render(request,"welcome.html",{"user":uname})
            return HttpResponseRedirect('/welcome/')
        # 登录失败
        else:
            #继续展示登录页面
            form = LoginForm()
            return render(request,'login.html',locals())

    # 处理get请求
    else:
        #判断session中是否有id 和　uphone
        if 'id' in request.session and 'uphone' in request.session:
            #session 中有登录信息　直接去首页
            return HttpResponseRedirect('/index/')
        else:
            #session中没有登录信息
            if 'id' in request.COOKIES and 'uphone' in request.COOKIES:
                #曾经登陆过　而且保存了信息　取出数据保存进session
                uid = request.COOKIES['id']
                uphone = request.COOKIES['uphone']
                request.session['id'] = uid
                request.session['uphone'] = uphone
                return HttpResponseRedirect('/index/')
            # cookies中也没有登录信息
            else:
                form = LoginForm()
                #将url保存进cookies
                return render(request,'login.html',locals())



#退出登录
def logout_views(request):
    if 'id' in request.session and 'uphone' in request.session:
        #将id和uphone的值从session中移除出去
        del request.session['id']
        del request.session['uphone']
        #记录源地址
        # url = request.META.get('HTTP_REFERER','/')
        # print(url)
        resp = HttpResponseRedirect('/login/')
        #判断cookies是否包含登录信息，在决定是否删除
        if 'id' in request.COOKIES and 'uphone' in request.COOKIES:
            # print(request.COOKIES['id'])
            # print(request.COOKIES['uphone'])
            resp.delete_cookie('id')
            resp.delete_cookie('uphone')
        return resp
    return HttpResponseRedirect('/')


def welcome_views(request):
    id = request.session.get('id')
    print(id)
    uname = User.objects.get(id=id).uname
    print(uname)
    return render(request,"welcome.html",{"user":uname})


#-----------------------------------------------------------------------------------
#启动Jenkins服务
def timing_views(request):
    os.system("java -jar /Users/zhuzhanhao/jenkins.war")
    id = request.session.get('id')
    uname = User.objects.get(id=id).uname
    return render(request,"welcome.html",{"user":uname})

#启动jmeter
def performance_views(request):
    os.system("sh /Users/zhuzhanhao/apache-jmeter-5.1/bin/jmeter.sh")
    id = request.session.get('id')
    uname = User.objects.get(id=id).uname
    return render(request,"welcome.html",{"user":uname})



#-----------------------------------------------------------------------------------
# 首页
# @login_required
def index_views(request):
    # 验证session中是否包含登录信息
    if 'id' in request.session and 'uphone' in request.session:
        # 通过session的id来获取uname
        id = request.session.get('id')
        uname = User.objects.get(id=id).uname
        uList = Case.objects.all()
        return render(request,"index.html",{"user":uname,"cases":uList})
    else:
        #session中没有登入信息,查询COOKIES中是否包含登入信息
        if 'id' in request.COOKIES and 'uphone' in request.COOKIES:
            user_id = request.COOKIES['id']
            uphone = request.COOKIES['uphone']
            # 将user_id和uphone保存进session
            request.session['id'] = user_id
            request.session['uphone'] = uphone
            #查询uname的值响应给客户端
            uname = User.objects.get(id=user_id).uname
            return render(request,"index.html",{"user":uname})
        else:
            data = "Session过期"
            return render(request,"error404.html",{"message":data})


#创建用例
def create_case_views(request):
    id = request.session.get('id')
    uname = User.objects.get(id=id).uname
    all = Case.objects.all().order_by("caseid")
    if request.method == 'POST':
        ucasename = request.POST.get('casename','')
        uurl = request.POST.get('url','')
        umethod = request.POST.get('method','')
        ubelong = request.POST.get('belong','')
        L = []
        r1 = request.POST.get("r1","")
        r2 = request.POST.get("r2", "")
        r3 = request.POST.get("r3", "")
        L.append(r1)
        L.append(r2)
        L.append(r3)
        for i in L:
            if i != '':
                uradio = i
                print(uradio)
                uparams = request.POST.get('params','')
                ubody = request.POST.get('body', '')
                dic = {
                    'casename': ucasename,
                    'url': uurl,
                    'method': umethod,
                    'belong': ubelong,
                    'params': uparams,
                    'body': ubody,
                    "identity":uradio
                }
                print(dic)
                Case(**dic).save()
                messages.success(request, "创建用例成功")
                return render(request,"index.html",{"user":uname,"cases":all})


#按名字查询
def search_name_views(request):
    id = request.session.get('id')
    uname = User.objects.get(id=id).uname
    search_name = request.GET.get("casename", "")
    cases_list = Case.objects.filter(casename__contains=search_name)
    return render(request, "index.html", {"cases": cases_list,"user":uname})



#删除用例
def delete_case_views(request):
    id = request.session.get('id')
    uname = User.objects.get(id=id).uname
    uList = Case.objects.all()
    print("ssssssssss")
    ucaseid = request.POST.get("caseid","")
    print(ucaseid)
    Case.objects.get(caseid=ucaseid).delete()
    messages.success(request,"删除用例成功")
    return render(request,"index.html",{"cases":uList,"user":uname})


#更新用例
def update_case_views(request):
    id = request.session.get('id')
    uname = User.objects.get(id=id).uname
    all = Case.objects.all().order_by("caseid")
    if request.method == 'POST':
        ucaseid = request.POST.get('caseid','')
        print(ucaseid)
        ucasename = request.POST.get('casename','')
        uurl = request.POST.get('url','')
        umethod = request.POST.get('method','')
        ubelong = request.POST.get("belong","")
        uparams = request.POST.get("params", "")
        ubody = request.POST.get("body", "")
        L = []
        r1 = request.POST.get("r1","")
        r2 = request.POST.get("r2", "")
        r3 = request.POST.get("r3", "")
        L.append(r1)
        L.append(r2)
        L.append(r3)
        for i in L:
            if i :
                uidentity = i
                print(uidentity)
                Case.objects.filter(caseid=ucaseid).update(casename=ucasename,identity=uidentity,url=uurl,method=umethod,belong=ubelong,params=uparams,body=ubody)
                return render(request,"index.html",{"user":uname,"cases":all})
            else:
                Case.objects.filter(caseid=ucaseid).update(casename=ucasename,url=uurl,method=umethod,belong=ubelong,params=uparams,body=ubody)
                return render(request,"index.html",{"user":uname,"cases":all})



#导入用例
def import_case_views(request):
    if request.method == 'POST':
        f = request.FILES.get('file')
        excel_type = f.name.split('.')[1]
        if excel_type in ['xlsx','xls']:
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None,file_contents=f.read())
            table = wb.sheets()[0]
            rows = table.nrows  # 总行数
            print(rows)
            try:
                with transaction.atomic():  # 控制数据库事务交易
                    for i in range(1,rows):
                        rowVlaues = table.row_values(i)
                        print(rowVlaues)
                        print(int(rowVlaues[0]))
                        # major = models.TMajor.objects.filter(majorid=rowVlaues[1]).first()
                        Case.objects.create(caseid=int(rowVlaues[0]),casename=rowVlaues[1],identity=rowVlaues[2],url=rowVlaues[3],method=rowVlaues[4],belong=rowVlaues[5],params=rowVlaues[6],body=rowVlaues[7])
                        print('插入成功')
            except:
                print('解析excel文件或者数据插入错误')
            messages.success(request, "导入用例成功")
            return JsonResponse({"status":200,"message":"导入数据成功"})
        else:
            print('上传文件类型错误！')
            return JsonResponse({"status":200,"message":"导入数据失败"})



#执行用例
def run_case_views(request):
    ucaseid = request.GET.get("caseid", "")
    uidentity = request.GET.get("identity","")
    all = Case.objects.all().order_by("caseid")
    id = Case.objects.filter(caseid=ucaseid).values()
    Runmethod = RequestMethod(uidentity)
    Header = ReqParam().get_user_power(uidentity)['accessToken']
    for i in id:
        url = "http://demo.amberdata.cn/ermsapi/v2"+i['url']
        method = i['method']
        params = i['params']
        if i["body"] != "" and params == "":
            body = eval(i["body"])
            casename = i['casename']
            belong = i['belong']
            identity = i['identity']
            response = Runmethod.run_main(method,url,params,body)
            print(response)
            dic = {
                "identity":identity,
                "belong":belong,
                "casename":casename,
                "url":url,
                "method":method,
                "params":params,
                "body":body,
                "header":Header
            }
            Case.objects.filter(caseid=ucaseid).update(result=response)
            return render(request,"result.html",{'response':response,"dic":dic})

        elif i["body"] != "" and params !=  "":
            body = eval(i["body"])
            params = eval(i['params'])
            casename = i['casename']
            belong = i['belong']
            identity = i['identity']
            response = Runmethod.run_main(method,url,params,body)
            print(response)
            dic = {
                "identity":identity,
                "belong":belong,
                "casename":casename,
                "url":url,
                "method":method,
                "params":params,
                "body":body,
                "header":Header
            }
            Case.objects.filter(caseid=ucaseid).update(result=response)
            return render(request,"result.html",{'response':response,"dic":dic})

        elif i["body"] == '':
            body = i["body"]
            casename = i['casename']
            belong = i['belong']
            identity = i['identity']
            if i['params']:
                params = eval(i["params"])
                response = Runmethod.run_main(method, url, params, body)
                print(response)
                dic = {
                    "identity": identity,
                    "belong": belong,
                    "casename": casename,
                    "url": url,
                    "method": method,
                    "params": params,
                    "body": body,
                    "header": Header
                }
                Case.objects.filter(caseid=ucaseid).update(result=response)
                # return render(request, "result.html", {'response': response,"cases":all})
                return render(request, "result.html", {'response': response, "dic": dic})
            else:
                response = Runmethod.run_main(method, url, params, body)
                print(response)
                dic = {
                    "identity": identity,
                    "belong": belong,
                    "casename": casename,
                    "url": url,
                    "method": method,
                    "params": params,
                    "body": body,
                    "header": Header
                }
                Case.objects.filter(caseid=ucaseid).update(result=response)
                return render(request, "result.html", {'response': response, "dic": dic})


#用例列表
def caselist_views(request):
    #从session中获取用户信息
    id = request.session.get('id')
    uname = User.objects.get(id=id).uname
    allcasecount = Case.objects.all()
    all_p = Paginator(allcasecount, 8)
    # res = Case.objects.filter()
    #列表展示-所有用例
    belong_model = request.GET.get('belong','')
    if belong_model == '':
        uList = Case.objects.all().order_by("caseid")
        #设置一页存在多少条用例
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":paginator})

    # 列表展示-单位接口
    elif belong_model == "unit":
        uList = Case.objects.filter(belong="单位接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"b":belong_model,'p1':paginator})


    # 列表展示-部门管理接口
    elif belong_model == "dept":
        uList = Case.objects.filter(belong="部门管理接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"b":belong_model,'p2':paginator})

    # 列表展示-用户模块接口
    elif belong_model == "user":
        uList = Case.objects.filter(belong="用户模块接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p3":paginator,"b":belong_model})


    # 列表展示-保留处置策略接口
    elif belong_model == "policy":
        uList = Case.objects.filter(belong="保留处置策略接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p4":paginator,"b":belong_model})


    # 列表展示-保留处置策略接口
    elif belong_model == "source":
        uList = Case.objects.filter(belong="档案来源接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p5":paginator,"b":belong_model})


    # 列表展示-元数据管理平台相关接口
    elif belong_model == "metadata":
        uList = Case.objects.filter(belong="元数据管理平台相关接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p6":paginator,"b":belong_model})


    # 列表展示-公共操作相关接口
    elif belong_model == "common":
        uList = Case.objects.filter(belong="公共操作相关接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p7":paginator,"b":belong_model})

    # 列表展示-导航管理接口
    elif belong_model == "navigation":
        uList = Case.objects.filter(belong="导航管理接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p8":paginator,"b":belong_model})

    # 列表展示-数据表单接口管理
    elif belong_model == "data_form":
        uList = Case.objects.filter(belong="数据表单管理接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p9":paginator,"b":belong_model})

    # 列表展示-数据表单配置管理接口
    elif belong_model == "data_form_config":
        uList = Case.objects.filter(belong="数据表单配置管理接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p10":paginator,"b":belong_model})

    # 列表展示-文件计划管理接口
    elif belong_model == "file_plan":
        uList = Case.objects.filter(belong="文件计划管理接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p11":paginator,"b":belong_model})

    # 列表展示-文档管理
    elif belong_model == "document":
        uList = Case.objects.filter(belong="文档管理").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p12":paginator,"b":belong_model})

    # 列表展示-Record接口
    elif belong_model == "record":
        uList = Case.objects.filter(belong="Record接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p13":paginator,"b":belong_model})

    # 列表展示-案卷管理
    elif belong_model == "volume":
        uList = Case.objects.filter(belong="案卷管理").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p14":paginator,"b":belong_model})

    # 列表展示-档案管理
    elif belong_model == "archives":
        uList = Case.objects.filter(belong="档案管理").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p15":paginator,"b":belong_model})

    # 列表展示-移交表单接口
    elif belong_model == "transfer_form":
        uList = Case.objects.filter(belong="移交表单接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p16":paginator,"b":belong_model})

    # 列表展示-类目模块17
    elif belong_model == "class":
        uList = Case.objects.filter(belong="类目模块接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p17":paginator,"b":belong_model})

    # 列表展示-视图自定义接口18
    elif belong_model == "view":
        uList = Case.objects.filter(belong="视图自定义接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p18":paginator,"b":belong_model})

    # 列表展示-角色管理19
    elif belong_model == "role":
        uList = Case.objects.filter(belong="角色管理").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p19":paginator,"b":belong_model})

    # 列表展示-访问控制权限模块20
    elif belong_model == "acl":
        uList = Case.objects.filter(belong="访问控制权限接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p20":paginator,"b":belong_model})

    # 列表展示-资源管理21
    elif belong_model == "resource":
        uList = Case.objects.filter(belong="资源管理").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p21":paginator,"b":belong_model})

    # 列表展示-通用文件夹管理22
    elif belong_model == "common_folder":
        uList = Case.objects.filter(belong="通用文件夹管理").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p22":paginator,"b":belong_model})

    # 列表展示-门类模块23
    elif belong_model == "category":
        uList = Case.objects.filter(belong="门类模块接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p23":paginator,"b":belong_model})

    # 列表展示-视图自定义接口
    elif belong_model == "view":
        uList = Case.objects.filter(belong="视图自定义接口").order_by("caseid")
        paginator = Paginator(uList, 8)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "index.html", {"user":uname,"cases": contacts,"all_p":all_p,"p18":paginator,"b":belong_model})


