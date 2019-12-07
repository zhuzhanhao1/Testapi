import django,os
#
# from django.test import TestCase
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver.chrome.webdriver import WebDriver
# import sys
# currentUrl = os.path.dirname(__file__)
# cur_path = os.path.abspath(os.path.join(currentUrl,os.pardir))
# sys.path.append(cur_path)
# from Api.models import Case,User
#
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Testapi.settings")# project_name 项目名称
# django.setup()
# class ModelTest(TestCase):
#     '''模型测试'''
#
#     def setUp(self):
#         User.objects.create(uphone="15158989710",uname="朱占豪",upwd="zhuzhanhao",uemail="971567069@qq.com")
#         Case.objects.create(caseid=3,casename="模型测试", identity="sysadmin", url="/unit/get_unit_by_group_name",
#                                method="get", params={"unitGroupName":"unit_j001"}, body="", belong="单位接口")
#
#     def test_User_models(self):
#         '''测试User表'''
#         retult = User.objects.get(Uname="朱占豪")
#         self.assertEqual(retult.uphone,"15158989710")
#
#     def test_Case_models(self):
#         '''测试caseapi表'''
#         retult = Case.objects.get(case="模型测试")
#         self.assertEqual(retult.caseid,3)
#
#
# class IndexPageTest(TestCase):
#     '''测试index登录首页'''
#
#     def test_index_page_renders_index_template(self):
#         ''' 断言是否用给定的index.html模版响应'''
#         response = self.client.get('/index/')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'index.html')
#
#
#
print("朱占豪测试")
