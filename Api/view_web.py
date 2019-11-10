import json
import unittest
import sys
import os
import xlrd
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# 本文件路径
from Api.models import Webcase, User, Autocase

currentUrl = os.path.dirname(__file__)
# 父文件路径
cur_path = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(cur_path)

from Api.webuitest.A_sysadmin_test import SystemManagement
from Api.webuitest.B_admin_test import UnitManagement
from Api.webuitest.C_ywsd_test import AstManagement
import Api.webuitest.htmlCN
from Api.webuitest.conn_database import ConnDataBase
from Api.webuitest.EmailSend import SendEmail
from Api.webuitest.DingDing import send_ding



# web首页
@login_required
def webindex_views(request):
    a = request.GET.get("belong", "")
    case_count = Webcase.objects.all().count()
    return render(request, "webindex.html", {"user": "朱占豪", "abq": a, "case_count": case_count})

# weB列表页
@login_required
def weblist_view(request):
    #所属模块
    system = request.GET.get("system", "")
    print(system)
    if system == "erms":
        module = request.GET.get("key[id]", "")
        print(module)
        a = request.GET.get("belong", "")
        filterSos = request.GET.get("filterSos", "")

        if module == "" and a == "" and filterSos== "":
            weblists = Webcase.objects.filter(system=system).order_by("webcase_models","webfunpoint")
        if a:
            if a == "policy":
                weblists = Webcase.objects.filter(Q(webcase_models="保留处置策略管理") & Q(system="erms"))
            elif a == "unit":
                weblists = Webcase.objects.filter(Q(webcase_models="入驻单位管理") & Q(system="erms"))
            elif a == "forms":
                weblists = Webcase.objects.filter(Q(webcase_models="数据表单设置") & Q(system="erms"))
            elif a == "views":
                weblists = Webcase.objects.filter(Q(webcase_models="视图管理") & Q(system="erms"))
            elif a == "info":
                weblists = Webcase.objects.filter(Q(webcase_models="基本信息") & Q(system="erms"))
            elif a == "dept":
                weblists = Webcase.objects.filter(Q(webcase_models="部门管理") & Q(system="erms"))
            elif a == "user":
                weblists = Webcase.objects.filter(Q(webcase_models="用户管理") & Q(system="erms"))
            elif a == "class":
                weblists = Webcase.objects.filter(Q(webcase_models="类目保管期限设定") & Q(system="erms"))
            elif a == "access":
                weblists = Webcase.objects.filter(Q(webcase_models="访问控制策略管理") & Q(system="erms"))
            elif a == "transfer":
                weblists = Webcase.objects.filter(Q(webcase_models="移交操作") & Q(system="erms"))
        elif module:
            try:
                if int(module):
                    weblists = Webcase.objects.filter(Q(webcaseid=module) & Q(system="erms")).order_by("webcase_models","webfunpoint")
            except:
                weblists = Webcase.objects.filter(Q(webcase_models__contains=module) & Q(system="erms")).order_by("webcase_models","webfunpoint")

        elif filterSos:
            print(filterSos)
            if filterSos == "[]":
                weblists = Webcase.objects.filter(system=system).order_by("webcase_models","webfunpoint")
            else:
                L = []
                for i in json.loads(filterSos):
                    filterSos_field = i.get("field")
                    filterSos_value = i.get("value")
                    if filterSos_field == "funpoint":
                        apilists = Webcase.objects.filter(Q(webfunpoint__contains=filterSos_value) & Q(system="erms")).order_by("webcase_models","webfunpoint")
                    elif filterSos_field == "module":
                        apilists = Webcase.objects.filter(Q(webcase_models__contains=filterSos_value) & Q(system="erms")).order_by("webcase_models","webfunpoint")
                    elif filterSos_field == "casename":
                        apilists = Webcase.objects.filter(Q(webcasename__contains=filterSos_value) & Q(system="erms")).order_by("webcase_models","webfunpoint")
                    for weblist in apilists:
                        data = {
                            "caseid": weblist.webcaseid,
                            "module": weblist.webcase_models,
                            "funpoint": weblist.webfunpoint,
                            "casename": weblist.webcasename,
                            "premise": weblist.webpremise,
                            "teststep": weblist.webteststep,
                            "exceptres": weblist.webexceptres,
                            "result": weblist.webresult,
                            "identity": weblist.webidentity,
                            "webbelong": weblist.webbelong
                        }
                        L.append(data)
                print(L)
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


    elif system == "transfer":
        module = request.GET.get("key[id]", "")
        print(module)
        a = request.GET.get("belong", "")
        filterSos = request.GET.get("filterSos", "")

        if module == "" and a == "" and filterSos== "":
            weblists = Webcase.objects.filter(system=system).order_by("webcase_models","webfunpoint")
        elif module:
            try:
                if int(module):
                    weblists = Webcase.objects.filter(Q(webcaseid=module) & Q(system="transfer")).order_by("webcase_models","webfunpoint")
            except:
                weblists = Webcase.objects.filter(Q(webcase_models__contains=module) & Q(system="transfer")).order_by("webcase_models","webfunpoint")

        elif filterSos:
            print(filterSos)
            if filterSos == "[]":
                weblists = Webcase.objects.filter(system=system).order_by("webcase_models","webfunpoint")
            else:
                L = []
                for i in json.loads(filterSos):
                    filterSos_field = i.get("field")
                    filterSos_value = i.get("value")
                    if filterSos_field == "funpoint":
                        apilists = Webcase.objects.filter(Q(webfunpoint__contains=filterSos_value) & Q(system="transfer")).order_by("webcase_models","webfunpoint")
                    elif filterSos_field == "module":
                        apilists = Webcase.objects.filter(Q(webcase_models__contains=filterSos_value) & Q(system="transfer")).order_by("webcase_models","webfunpoint")
                    elif filterSos_field == "casename":
                        apilists = Webcase.objects.filter(Q(webcasename__contains=filterSos_value) & Q(system="transfer")).order_by("webcase_models","webfunpoint")
                    for weblist in apilists:
                        data = {
                            "caseid": weblist.webcaseid,
                            "module": weblist.webcase_models,
                            "funpoint": weblist.webfunpoint,
                            "casename": weblist.webcasename,
                            "premise": weblist.webpremise,
                            "teststep": weblist.webteststep,
                            "exceptres": weblist.webexceptres,
                            "result": weblist.webresult,
                            "identity": weblist.webidentity,
                            "webbelong": weblist.webbelong
                        }
                        L.append(data)
                print(L)
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

    else:
        weblists = Webcase.objects.filter().order_by("webcase_models", "webfunpoint")

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
            "result": weblist.webresult,
            "identity": weblist.webidentity,
            "webbelong": weblist.webbelong
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


# 创建web用例
@login_required
def create_webcase_views(request):
    if request.method == 'POST':
        webname = request.POST.get("title", "")
        funpoint = request.POST.get("funpoint", "")
        mainbelong = request.POST.get("mainbelong", "")
        belong = request.POST.get("belong", "")
        premise = request.POST.get("premise", "")
        steps = request.POST.get("steps", "")
        exceptres = request.POST.get("except", "")
        system = request.POST.get("system", "")
        Webcase.objects.create(webcasename=webname, webbelong=mainbelong, webcase_models=belong,system=system,
                               webfunpoint=funpoint, webpremise=premise, webteststep=steps, webexceptres=exceptres)
        return HttpResponse("操作成功")

# 删除web用例
@login_required
def delete_webcase_views(request):
    if request.method == "GET":
        ids = request.GET.get("ids", "")
        print(ids)
        caseids = json.loads(ids)
        for caseid in caseids:
            Webcase.objects.filter(webcaseid=caseid.get("caseid","")).delete()
        return HttpResponse("删除成功")
        # if ids:
        #     print(ids)
        #     Webcase.objects.filter(webcaseid=ids).delete()
        #     return HttpResponse("删除成功")

# 更新web用例
@login_required
def update_webcase_views(request):
    if request.method == "GET":
        caseid = request.GET.get("ids", "")
        casename = request.GET.get("casename", "")
        teststep = request.GET.get("teststep", "")
        exceptres = request.GET.get("exceptres", "")
        result = request.GET.get("result", "")
        if casename:
            Webcase.objects.filter(webcaseid=caseid).update(webcasename=casename)
        elif teststep:
            Webcase.objects.filter(webcaseid=caseid).update(webteststep=teststep)
        elif exceptres:
            Webcase.objects.filter(webcaseid=caseid).update(webexceptres=exceptres)
        elif result:
            Webcase.objects.filter(webcaseid=caseid).update(webresult=result)
        return HttpResponse("操作成功")

    if request.method == "POST":
        mainbelong = request.POST.get("mainbelong", "")
        belong = request.POST.get("belong", "")
        funpoint = request.POST.get("funpoint", "")
        title = request.POST.get("title", "")
        premise = request.POST.get("premise", "")
        steps = request.POST.get("steps", "")
        exceptres = request.POST.get("except", "")
        caseID = request.POST.get("caseID", "")
        Webcase.objects.filter(webcaseid=caseID).update(webteststep=steps, webcase_models=belong, webcasename=title,
                                                        webfunpoint=funpoint, webpremise=premise,
                                                        webexceptres=exceptres, webbelong=mainbelong)
        return HttpResponse("操作成功")

# 导入用例
@login_required
def import_webcase_views(request):
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
                        Webcase.objects.create(webbelong=rowVlaues[0],webcase_models=rowVlaues[1],
                                               webfunpoint=rowVlaues[2], webcasename=rowVlaues[3],
                                               webpremise=rowVlaues[4], webteststep=rowVlaues[5],
                                               webexceptres=rowVlaues[6],system=rowVlaues[7])
                        print('插入成功')
            except:
                print('解析excel文件或者数据插入错误')
                return HttpResponse("Failed!!!")
            return HttpResponse("ok success!请按浏览器的返回键返回，由于请求通过form表单中，html input 标签的“file”完成，没采用ajax请求。")
            # return JsonResponse({"status":200,"message":"导入数据成功"})
        else:
            print('上传文件类型错误！')
            return JsonResponse({"status": 200, "message": "导入数据失败"})

# -----------------------------------------------------------------------------------

# Auto列表页
@login_required
def antolist_view(request):
    caseid = request.GET.get("key[id]", "")
    weblists = Autocase.objects.filter().order_by("sortid")
    a = request.GET.get("belong","")
    b = request.GET.get("system","")
    L = []
    if caseid:
        weblists = Autocase.objects.filter(autoid=caseid)
    if b == "erms":
        if a:
            if a == "dataform":
                weblists = Autocase.objects.filter(Q(autobelong="数据表单设置") & Q(system="erms"))
            elif a == "unit":
                weblists = Autocase.objects.filter(Q(autobelong="入驻单位管理") & Q(system="erms"))
            elif a == "policy":
                weblists = Autocase.objects.filter(Q(autobelong="保留处置策略管理") & Q(system="erms"))
            elif a == "dept":
                weblists = Autocase.objects.filter(Q(autobelong="部门管理") & Q(system="erms"))
            elif a == "user":
                weblists = Autocase.objects.filter(Q(autobelong="用户管理") & Q(system="erms"))
            elif a == "acl":
                weblists = Autocase.objects.filter(Q(autobelong="访问控制策略") & Q(system="erms"))
    for weblist in weblists:
        data = {
            "caseid": weblist.autoid,
            "module": weblist.autobelong,
            "casename": weblist.autoname,
            "identity": weblist.autoidentity,
            "dataready": weblist.autodataready,
            "teststep": weblist.autostep,
            "exceptres": weblist.autoexceptres,
            "result": weblist.autoresult,
            "sortid":weblist.sortid
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


# 创建webAuto用例
@login_required
def create_autocase_views(request):
    if request.method == 'POST':
        autoname = request.POST.get("title", "")
        belong = request.POST.get("belong", "")
        idnetity = request.POST.get("identity", "")
        dataready = request.POST.get("dataready", "")
        steps = request.POST.get("steps", "")
        exceptres = request.POST.get("except", "")
        Autocase.objects.create(autoname=autoname, autobelong=belong, autoidentity=idnetity, autodataready=dataready,
                                autostep=steps, autoexceptres=exceptres)
        return HttpResponse("操作成功")


# 删除webAuto用例
@login_required
def delete_autocase_views(request):
    if request.method == "GET":
        ids = request.GET.get("ids", "")
        if ids:
            print(ids)
            Autocase.objects.filter(autoid=ids).delete()
            return HttpResponse("删除成功")


# 更新webauto用例
@login_required
def update_autocase_views(request):
    if request.method == "GET":
        steps = request.GET.get('steps', "")
        result = request.GET.get("result", "")
        ids = request.GET.get("ids", "")
        dataready = request.GET.get("body", "")
        print(ids)
        if result:
            print(result)
            if result == "1":
                Autocase.objects.filter(autoid=ids).update(autoresult="")
            else:
                Autocase.objects.filter(autoid=ids).update(autoresult=result)
            return HttpResponse("编辑成功")
        elif dataready:
            data = json.dumps(eval(dataready), ensure_ascii=False, sort_keys=True, indent=2)
            print(data)
            if dataready == "1":
                Autocase.objects.filter(autoid=ids).update(autodataready="")
            else:
                Autocase.objects.filter(autoid=ids).update(autodataready=data)
            return HttpResponse("编辑成功")


    else:
        belong = request.POST.get("belong", "")
        identity = request.POST.get("identity", "")
        dataready = request.POST.get("dataready", "")
        title = request.POST.get("title", "")
        steps = request.POST.get("steps", "")
        exceptres = request.POST.get("except", "")
        caseID = request.POST.get("caseID", "")
        Autocase.objects.filter(autoid=caseID).update(autostep=steps, autoname=title, autoidentity=identity,
                                                      autobelong=belong, autoexceptres=exceptres,
                                                      autodataready=dataready)
        return HttpResponse("操作成功")


# 测试报告
@login_required
def report_webcase_views(request):
    return render(request, "TestReport.html")


# 获取当前用户信息
@login_required
def get_userinfo_views(request):
    con = ConnDataBase()
    sysadmin = con.get_logininfo("uisysadmin")
    admin = con.get_logininfo("uiadmin")
    ast = con.get_logininfo("uiast")
    dic = {
        "系统管理员": {
            "账号": sysadmin[0],
            "密码": sysadmin[1],
        },
        "单位管理员": {
            "账号": admin[0],
            "密码": admin[1],
        },
        "单位档案员": {
            "账号": ast[0],
            "密码": ast[1],
        },
    }
    dic1 = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=2)
    print(dic1)
    return HttpResponse(dic1)


# 排序
@login_required
def autosort_views(request):
    if request.method == "GET":
        oldIndex = int(request.GET.get("oldIndex",""))+1
        newIndex = int(request.GET.get("newIndex", ""))+1
        if oldIndex < newIndex:
            q = []
            for i in range(oldIndex,newIndex):
                a = i + 1
                for b in Autocase.objects.filter(sortid=a):
                    q.append(b.autoid)
                Autocase.objects.filter(sortid=a).update(sortid=i)
            l = Autocase.objects.filter(sortid=oldIndex)
            for lll in l:
                if lll.autoid not in q:
                    Autocase.objects.filter(autoid=lll.autoid).update(sortid=newIndex)
        elif oldIndex > newIndex:
            Autocase.objects.filter(sortid=oldIndex).update(sortid=-1)
            L = []
            for i in range(newIndex,oldIndex):
                L.append(i)
            e = L[::-1]
            for r in e:
                Autocase.objects.filter(sortid=r).update(sortid=r+1)
            Autocase.objects.filter(sortid=-1).update(sortid=newIndex)
        return HttpResponse("排序成功")



# 运行webAuto测试用例
@login_required
def run_autocase_views(request):
    ids = request.GET.get("ids").split(",")[:-1]
    print(ids)
    suite = unittest.TestSuite()
    for id in ids:
        data = Autocase.objects.get(autoid=id)
        print(data.autoname)
        # 入驻单位管理
        if data.autoname == "新建单位":
            suite.addTest(SystemManagement('test_a_unit_create'))
        elif data.autoname == "编辑单位":
            suite.addTest(SystemManagement('test_b_unit_update'))
        elif data.autoname == "删除单位":
            suite.addTest(SystemManagement('test_c_unit_delete'))
        # 保留处置策略管理
        elif data.autoname == "新建保留处置策略":
            suite.addTest(SystemManagement('test_d_policy_create'))
        elif data.autoname == "编辑保留处置策略":
            suite.addTest(SystemManagement('test_e_policy_update'))
        elif data.autoname == "删除保留处置策略":
            suite.addTest(SystemManagement('test_f_policy_delete'))
        # 数据表单设置
        elif data.autoname == "新建数据表单":
            suite.addTest(SystemManagement('test_a_forms_create'))
        elif data.autoname == "删除数据表单":
            suite.addTest(SystemManagement('test_a_forms_delete'))
        # 部门管理
        elif data.autoname == "新建部门":
            suite.addTest(UnitManagement('test_b_create_dept'))
        elif data.autoname == "编辑部门":
            suite.addTest(UnitManagement('test_c_update_dept'))
        elif data.autoname == "删除部门":
            suite.addTest(UnitManagement('test_d_delete_dept'))
        # 用户管理
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
        # 访问控制策略管理
        elif data.autoname == "新建访问控制策略":
            suite.addTest(AstManagement('test_ca_access_create'))
        elif data.autoname == "编辑访问控制策略":
            suite.addTest(AstManagement('test_cb_access_update'))
        elif data.autoname == "删除访问控制策略":
            suite.addTest(AstManagement('test_cc_access_delete'))
        # 档案员保留处置策略
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
    # 发送钉钉消息
    # send_ding("自动化测试已完成，具体内容请查收邮件")
    # 发送QQ邮件
    # SendEmail().send_main("自动化测试")
    return HttpResponse("操作完成")

#定义类-生成测试报告
class AllTest:
    def __init__(self):
        self.cur_path = os.path.dirname(os.path.realpath(__file__))

    def add_case(self, caseName='case', rule='*test.py'):
        # 加载所有用例
        case_path = os.path.join(self.cur_path, caseName)
        # 如果不存在这个case文件夹，就自动创建一个
        if not os.path.exists(case_path):
            os.mkdir(case_path)
        print('测试用例的路径为:%s' % case_path)
        discover = unittest.defaultTestLoader.discover(case_path, pattern=rule, top_level_dir=None)
        print(discover)
        return discover

    def run_case(self, all_case, reportName='templates'):
        # 报告文件夹
        report_path = os.path.join(self.cur_path, reportName)
        if not os.path.exists(report_path):
            os.mkdir(report_path)
        report_abspath = os.path.join(report_path, 'TestReport.html')
        print("测试报告的路径为:{}".format(report_abspath))
        with open(report_abspath, 'wb') as report_file:
            runner = Api.webuitest.htmlCN.HTMLTestRunner(stream=report_file,
                                                         title=u"ERMS自动化测试报告",
                                                         verbosity=2,
                                                         description='Web Automation Testingweb',
                                                         tester=u"朱占豪")
            runner.run(all_case)


