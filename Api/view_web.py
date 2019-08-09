import unittest
import sys
import os
import xlrd
from django.db import transaction
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

#本文件路径
from Api.models import Webcase, User, Autocase

currentUrl = os.path.dirname(__file__)
sys.path.append(currentUrl)
print(currentUrl)
#父文件路径
cur_path = os.path.abspath(os.path.join(currentUrl,os.pardir))
print(cur_path)
sys.path.append(cur_path)
from Api.webuitest.A_sysadmin_test import SystemManagement
from Api.webuitest.B_admin_test import UnitManagement
from Api.webuitest.C_ywsd_test import AstManagement
import Api.webuitest.htmlCN
from Api.webuitest.EmailSend import SendEmail
from Api.webuitest.DingDing import send_ding


class AllTest:
    def __init__(self):
        self.cur_path = os.path.dirname(os.path.realpath(__file__))

    def add_case(self,caseName='case',rule='*test.py'):
        #加载所有用例
        case_path = os.path.join(self.cur_path, caseName)
        #如果不存在这个case文件夹，就自动创建一个
        if not os.path.exists(case_path):
            os.mkdir(case_path)
        print('测试用例的路径为:%s'%case_path)
        discover = unittest.defaultTestLoader.discover(case_path,pattern=rule,top_level_dir=None)
        print(discover)
        return discover

    def run_case(self,all_case,reportName='templates'):
        # 报告文件夹
        report_path = os.path.join(self.cur_path,reportName)
        if not os.path.exists(report_path):
            os.mkdir(report_path)
        report_abspath = os.path.join(report_path,'TestReport.html')
        print("测试报告的路径为:{}".format(report_abspath))
        with open(report_abspath,'wb') as report_file:
            runner= Api.webuitest.htmlCN.HTMLTestRunner(stream=report_file,
                                          title=u"ERMS自动化测试报告",
                                          verbosity=2,
                                          description='Web Automation Testingweb',
                                          tester=u"朱占豪")
            runner.run(all_case)

#运行web测试用例
def run_webcase_views(request):
    ids = request.GET.get("ids").split(",")[:-1]
    print(ids)
    suite = unittest.TestSuite()
    for id in ids:
        data = Webcase.objects.get(webcaseid=id)
        #入驻单位管理
        if data.webfunpoint == "新建单位":
            suite.addTest(SystemManagement('test_a_unit_create'))
        elif data.webfunpoint == "编辑单位":
            suite.addTest(SystemManagement('test_b_unit_update'))
        elif data.webfunpoint == "删除单位":
            suite.addTest(SystemManagement('test_c_unit_delete'))
        #保留处置策略管理
        elif data.webfunpoint == "新建保留处置策略":
            suite.addTest(SystemManagement('test_d_policy_create'))
        elif data.webfunpoint == "编辑保留处置策略":
            suite.addTest(SystemManagement('test_e_policy_update'))
        elif data.webfunpoint == "删除保留处置策略":
            suite.addTest(SystemManagement('test_f_policy_delete'))

        #数据表单设置
        elif data.webfunpoint == "新建数据表单":
            suite.addTest(SystemManagement('test_a_forms_create'))
        elif data.webfunpoint == "删除数据表单":
            suite.addTest(SystemManagement('test_a_forms_delete'))

        #部门管理
        elif data.webfunpoint == "新建部门":
            suite.addTest(UnitManagement('test_b_create_dept'))
        elif data.webfunpoint == "编辑部门":
            suite.addTest(UnitManagement('test_c_update_dept'))
        elif data.webfunpoint == "删除部门":
            suite.addTest(UnitManagement('test_d_delete_dept'))
        #用户管理
        elif data.webfunpoint == "新建用户":
            suite.addTest(UnitManagement('test_e_user_create'))
        elif data.webfunpoint == "编辑用户":
            suite.addTest(UnitManagement('test_f_user_update'))
        elif data.webfunpoint == "导入用户":
            suite.addTest(UnitManagement('test_j_user_upload'))
        elif data.webfunpoint == "冻结用户":
            suite.addTest(UnitManagement('test_g_user_freeze'))
        elif data.webfunpoint == "激活用户":
            suite.addTest(UnitManagement('test_h_user_restore'))
        elif data.webfunpoint == "搜索用户":
            suite.addTest(UnitManagement('test_i_user_search'))
        #访问控制策略管理
        elif data.webfunpoint == "新建访问控制策略":
            suite.addTest(AstManagement('test_ca_access_create'))
        elif data.webfunpoint == "编辑访问控制策略":
            suite.addTest(AstManagement('test_cb_access_update'))
        elif data.webfunpoint == "删除访问控制策略":
            suite.addTest(AstManagement('test_cc_access_delete'))
        #档案员保留处置策略
        # elif data.webfunpoint == "新建保留处置策略":
        #     suite.addTest(AstManagement('test_da_policy_create'))
        # elif data.webfunpoint == "编辑保留处置策略":
        #     suite.addTest(AstManagement('test_db_policy_update'))
        # elif data.webfunpoint == "删除保留处置策略":
        #     suite.addTest(AstManagement('test_dc_policy_delete'))

        # runner = unittest.TextTestRunner(verbosity=2)
        # runner.run(suite)

    # 执行用例生成报告
    AllTest().run_case(suite)
    #发送钉钉消息
    # send_ding("自动化测试已完成，具体内容请查收邮件")
    #发送QQ邮件
    # SendEmail().send_main("自动化测试")
    return HttpResponse("操作完成")


#运行webAuto测试用例
def run_autocase_views(request):
    ids = request.GET.get("ids").split(",")[:-1]
    print(ids)
    suite = unittest.TestSuite()
    for id in ids:
        data = Autocase.objects.get(autoid=id)
        print(data.autoname)
        #入驻单位管理
        if data.autoname == "新建单位":
            suite.addTest(SystemManagement('test_a_unit_create'))
        elif data.autoname == "编辑单位":
            suite.addTest(SystemManagement('test_b_unit_update'))
        elif data.autoname == "删除单位":
            suite.addTest(SystemManagement('test_c_unit_delete'))
        #保留处置策略管理
        elif data.autoname == "新建保留处置策略":
            suite.addTest(SystemManagement('test_d_policy_create'))
        elif data.autoname == "编辑保留处置策略":
            suite.addTest(SystemManagement('test_e_policy_update'))
        elif data.autoname == "删除保留处置策略":
            suite.addTest(SystemManagement('test_f_policy_delete'))
        #数据表单设置
        elif data.autoname == "新建数据表单":
            suite.addTest(SystemManagement('test_a_forms_create'))
        elif data.autoname == "删除数据表单":
            suite.addTest(SystemManagement('test_a_forms_delete'))
        #部门管理
        elif data.autoname == "新建部门":
            suite.addTest(UnitManagement('test_b_create_dept'))
        elif data.autoname == "编辑部门":
            suite.addTest(UnitManagement('test_c_update_dept'))
        elif data.autoname == "删除部门":
            suite.addTest(UnitManagement('test_d_delete_dept'))
        #用户管理
        elif data.autoname == "新建用户":
            suite.addTest(UnitManagement('test_e_user_create'))
        elif data.autoname == "编辑用户":
            suite.addTest(UnitManagement('test_f_user_update'))
        elif data.autoname == "导入用户":
            suite.addTest(UnitManagement('test_j_user_upload'))
        elif data.autoname == "冻结用户":
            suite.addTest(UnitManagement('test_g_user_freeze'))
        elif data.autoname == "激活用户":
            suite.addTest(UnitManagement('test_h_user_restore'))
        elif data.autoname == "搜索用户":
            suite.addTest(UnitManagement('test_i_user_search'))
        #访问控制策略管理
        elif data.autoname == "新建访问控制策略":
            suite.addTest(AstManagement('test_ca_access_create'))
        elif data.autoname == "编辑访问控制策略":
            suite.addTest(AstManagement('test_cb_access_update'))
        elif data.autoname == "删除访问控制策略":
            suite.addTest(AstManagement('test_cc_access_delete'))
        #档案员保留处置策略
        # elif data.webfunpoint == "新建保留处置策略":
        #     suite.addTest(AstManagement('test_da_policy_create'))
        # elif data.webfunpoint == "编辑保留处置策略":
        #     suite.addTest(AstManagement('test_db_policy_update'))
        # elif data.webfunpoint == "删除保留处置策略":
        #     suite.addTest(AstManagement('test_dc_policy_delete'))

        # runner = unittest.TextTestRunner(verbosity=2)
        # runner.run(suite)

    # 执行用例生成报告
    AllTest().run_case(suite)
    #发送钉钉消息
    # send_ding("自动化测试已完成，具体内容请查收邮件")
    #发送QQ邮件
    # SendEmail().send_main("自动化测试")
    return HttpResponse("操作完成")



#-----------------------------------------------------------------------------------
#web首页
def webindex_views(request):
    id = request.session.get('id')
    uname = User.objects.get(id=id).uname
    a = request.GET.get("belong","")
    case_count = Webcase.objects.all().count()
    return render(request,"webindex.html",{"user":uname,"abq":a,"case_count":case_count})



#weB列表页
def weblist_view(request):
    module = request.GET.get("key[id]", "")
    caseid= request.GET.get("key[id1]","")
    a = request.GET.get("belong","")
    if module == "" and a == "" and caseid == "":
        weblists = Webcase.objects.filter()
    elif a == "policy":
        weblists = Webcase.objects.filter(webcase_models="保留处置策略管理")
    elif a == "unit":
        weblists = Webcase.objects.filter(webcase_models__contains="入驻单位管理")
    elif a == "forms":
        weblists = Webcase.objects.filter(webcase_models="数据表单设置")
    elif a == "views":
        weblists = Webcase.objects.filter(webcase_models="视图管理")
    elif a == "info":
        weblists = Webcase.objects.filter(webcase_models="基本信息")
    elif a == "dept":
        weblists = Webcase.objects.filter(webcase_models="部门管理")
    elif a == "user":
        weblists = Webcase.objects.filter(webcase_models="用户管理")
    elif a == "class":
        weblists = Webcase.objects.filter(webcase_models="类目保管期限设定")
    elif a == "access":
        weblists = Webcase.objects.filter(webcase_models="访问控制策略管理")
    elif a == "transfer":
        weblists = Webcase.objects.filter(webcase_models="移交操作")
    elif module:
        weblists = Webcase.objects.filter(webcase_models__contains=module)
    elif caseid:
        weblists = Webcase.objects.filter(webcaseid=caseid)
    L = []
    for weblist in weblists:
        data = {
            "caseid": weblist.webcaseid,
            "module": weblist.webcase_models,
            "funpoint": weblist.webfunpoint,
            "casename": weblist.webcasename,
            "premise": weblist.webpremise,
            "teststep": weblist.webteststep,
            "exceptres": weblist.webexceptres,
            "result": weblist.webresult
        }
        L.append(data)
    print(len(L))
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



#Auto列表页
def antolist_view(request):
    module = request.GET.get("key[id]", "")
    caseid= request.GET.get("key[id1]","")
    a = request.GET.get("belong","")
    if module == "" and a == "" and caseid == "":
        weblists = Autocase.objects.filter()
    elif a == "policy":
        weblists = Autocase.objects.filter(webcase_models="保留处置策略管理")
    elif a == "unit":
        weblists = Autocase.objects.filter(webcase_models__contains="入驻单位管理")
    elif a == "forms":
        weblists = Autocase.objects.filter(webcase_models="数据表单设置")
    elif a == "views":
        weblists = Autocase.objects.filter(webcase_models="视图管理")
    elif a == "info":
        weblists = Autocase.objects.filter(webcase_models="基本信息")
    elif a == "dept":
        weblists = Autocase.objects.filter(webcase_models="部门管理")
    elif a == "user":
        weblists = Autocase.objects.filter(webcase_models="用户管理")
    elif a == "class":
        weblists = Autocase.objects.filter(webcase_models="类目保管期限设定")
    elif a == "access":
        weblists = Autocase.objects.filter(webcase_models="访问控制策略管理")
    elif a == "transfer":
        weblists = Autocase.objects.filter(webcase_models="移交操作")
    elif module:
        weblists = Autocase.objects.filter(webcase_models__contains=module)
    elif caseid:
        weblists = Autocase.objects.filter(webcaseid=caseid)
    L = []
    for weblist in weblists:
        data = {
            "caseid": weblist.autoid,
            "module": weblist.autobelong,
            "casename": weblist.autoname,
            "identity":weblist.autoidentity,
            "dataready": weblist.autodataready,
            "teststep": weblist.autostep,
            "exceptres": weblist.autoexceptres,
            "result": weblist.autoresult
        }
        L.append(data)
    print(len(L))
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


#创建web用例
def create_webcase_views(request):
    if request.method == 'POST':
        webname = request.POST.get("title","")
        funpoint = request.POST.get("funpoint", "")
        mainbelong = request.POST.get("mainbelong","")
        belong = request.POST.get("belong","")
        idnetity = request.POST.get("identity","")
        premise = request.POST.get("premise","")
        steps = request.POST.get("steps","")
        exceptres =request.POST.get("except","")
        Webcase.objects.create(webcasename=webname,webbelong=mainbelong,webcase_models=belong,webidentity=idnetity,\
                               webfunpoint=funpoint,webpremise=premise,webteststep=steps,webexceptres=exceptres)
        return HttpResponseRedirect("/webindex/")


#创建webAuto用例
def create_autocase_views(request):
    if request.method == 'POST':
        autoname = request.POST.get("title","")
        belong = request.POST.get("belong","")
        idnetity = request.POST.get("identity","")
        dataready = request.POST.get("dataready","")
        steps = request.POST.get("steps","")
        exceptres =request.POST.get("except","")
        Autocase.objects.create(autoname=autoname,autobelong=belong,autoidentity=idnetity,autodataready=dataready,autostep=steps,autoexceptres=exceptres)
        return HttpResponseRedirect("/webindex/")


#删除web用例
def delete_webcase_views(request):
    if request.method == "GET":
        ids = request.GET.get("ids","")
        if ids:
            print(ids)
            Webcase.objects.filter(webcaseid=ids).delete()
            return HttpResponse("删除成功")


#删除webAuto用例
def delete_autocase_views(request):
    if request.method == "GET":
        ids = request.GET.get("ids","")
        if ids:
            print(ids)
            Autocase.objects.filter(autoid=ids).delete()
            return HttpResponse("删除成功")

#更新web用例
def update_webcase_views(request):
    if request.method == "GET":
        steps = request.GET.get('steps',"")
        result =request.GET.get("result","")
        ids = request.GET.get("ids","")
        print(ids)
        if steps:
            a = eval(steps)
            step = a["teststep"]
            webname = a["casename"]
            belong = a["module"]
            funpoint = a["funpoint"]
            premise = a["premise"]
            exceptres = a["exceptres"]
            result = a["result"]
            print(step)
            print(webname)
            print(belong)
            print(funpoint)
            print(premise)
            print(exceptres)
            print(result)
            Webcase.objects.filter(webcaseid=ids).update(webteststep=step,webcasename=webname,\
            webcase_models=belong,webfunpoint=funpoint,webpremise=premise,webexceptres=exceptres,webresult=result)
            return HttpResponse("编辑成功")
        elif result:
            print(result)
            if result == "null":
                Webcase.objects.filter(webcaseid=ids).update(webresult="")
            else:
                Webcase.objects.filter(webcaseid=ids).update(webresult=result)
            return HttpResponse("编辑成功")


#更新webauto用例
def update_autocase_views(request):
    if request.method == "GET":
        steps = request.GET.get('steps',"")
        result =request.GET.get("result","")
        ids = request.GET.get("ids","")
        print(ids)
        if steps:
            a = eval(steps)
            step = a["teststep"]
            webname = a["casename"]
            belong = a["module"]
            identity = a["identity"]
            premise = a["dataready"]
            exceptres = a["exceptres"]
            result = a["result"]
            print(step)
            print(webname)
            print(belong)
            print(premise)
            print(exceptres)
            print(result)
            Autocase.objects.filter(autoid=ids).update(autostep=step,autoname=webname,autoidentity=identity,\
                autobelong=belong,autodataready=premise,autoexceptres=exceptres,autoresult=result)
            return HttpResponse("编辑成功")
        elif result:
            print(result)
            if result == "null":
                Autocase.objects.filter(autoid=ids).update(autoresult="")
            else:
                Autocase.objects.filter(autoid=ids).update(autoresult=result)
            return HttpResponse("编辑成功")

#导入用例
def import_webcase_views(request):
    if request.method == 'POST':
        f = request.FILES.get('file')
        print(f)
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
                        Webcase.objects.create(webcaseid=int(rowVlaues[0]),webbelong=rowVlaues[1],webcase_models=rowVlaues[2],\
                        webfunpoint=rowVlaues[3],webcasename=rowVlaues[4],webpremise=rowVlaues[5],webteststep=rowVlaues[6],webexceptres=rowVlaues[7])
                        print('插入成功')
            except:
                print('解析excel文件或者数据插入错误')
                return HttpResponse("Failed!!!")
            return HttpResponse("ok success!!!")
            # return JsonResponse({"status":200,"message":"导入数据成功"})
        else:
            print('上传文件类型错误！')
            return JsonResponse({"status":200,"message":"导入数据失败"})


#测试报告
def report_webcase_views(request):
    return render(request,"TestReport.html")

