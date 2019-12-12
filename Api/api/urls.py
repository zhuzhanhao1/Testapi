from django.conf.urls import url
import os
import sys
currentUrl = os.path.dirname(__file__)
cur_path = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(cur_path)

from .view_process import *
from .views import *
from .view_web import *
from .view_api import *

urlpatterns = [
    #登入登出
    url(r'^login/$',login_views),
    url(r'^logout/$',logout_views),
    #系统首页
    url(r'^welcome/$',welcome_views),
    #接口快速测试页-Jenkins-jmeter
    url(r'^quickTest/$',quickTest_views),
    url(r'^timing/$', timing_views),
    url(r'^performance/$', performance_views),

#----------------------公共接口-----------------------------
    #获取当前用户信息-编辑用户信息-更改token
    url(r'^get_userinfo/$', get_userinfo_views),
    url(r'^update_userinfo_api/$',update_userinfo_api_views),
    url(r'^update_token_api/$', update_token_api_views),
    #发送钉钉通知
    url(r'^ding_ding/$',ding_ding_view),


#----------------------接口测试-----------------------------
    #接口首页-接口列表
    url(r'^apiindex/$', apiindex_view),
    url(r'^apilist/$', apilist_view),
    #接口的查看详情-增删改
    url(r'^get_apicase_details/$',get_apicase_details_views),
    url(r'^create_apicase/$', create_apicase_views),
    url(r'^del_apicase/$', delete_apicase_views),
    url(r'^update_apicase/$', update_apicase_views),
    #执行单一接口
    url(r'^run_apicase/$', run_apicase_views),

    #导入导出，导出数据的接口不用后台的，调用前台方法
    url(r'^import_case/$',import_apicase_views),
    url(r'^export_data/$',export_data_views),
    #接口字段详情
    url(r'^field_apilist/$',field_apilist_views),
    #单一接口列表排序
    url(r'^web_sort/$', web_sort_views),
    # 流程执行进度条
    url(r'^show_api/$', show_api_views),
    #重复执行
    url(r'^repeatrun_api/$', repeatrun_api_views),
    #检索用例
    url(r'^search', search_views),


#----------------------接口流程测试-----------------------------
    #流程测试-接口列表
    url(r'^processlist/$', processlist_view),
    #流程接口的查看详情-增删改
    url(r'^get_processcase_details/$',get_processcase_details_views),
    url(r'^create_processcase/$', create_processcase_views),
    url(r'^del_processcase/$', delete_processcase_views),
    url(r'^update_processcase/$', update_processcase_views),
    #运行流程测试-定时任务
    url(r'^run_processcase/$', run_processcase_views),
    url(r'^timetask/$',timetask_views),
    #流程接口列表排序
    url(r'^process_sort/$', process_sort_views),
    #流程执行进度条
    url(r'^show_progress/$', show_progress_views),
    #重复执行
    url(r'^repeatrun/$', repeatrun_views),
    #流程结果
    url(r'^process_result/$', process_result_views),
    #流程结果列表
    url(r'^process_result_list', process_result_list_views),


    # 测试系统V2版首页
    url(r'^web_index/$', web_index_views),
    url(r'^web_welcome/$', web_welcome_views),
    # 接口测试首页
    url(r'^web_apiindex/$', web_apiindex_views),
    # 单一接口快速测试首页
    url(r'^web_quicktest/$', web_quicktest_views),
    # 功能测试首页
    url(r'^web_functionalTest/$', web_functionalTest_views),
    # 自动化UI测试首页
    url(r'^web_autoindex/$', web_autoTest_views),
    # 个人信息首页
    url(r'^web_info/$', web_info_views),
    # 友情链接首页
    url(r'^web_linklist/$', web_linklist_views),
    # 测试网址首页
    url(r'^web_linktest/$', web_linktest_views),
    # 流程接口测试首页
    url(r'^web_process/$', web_process_views),


    #----------------------web url-----------------------------
    # url(r'^webindex/$',webindex_views),
    #功能测试用例
    url(r'^weblist/$',weblist_view),
    #用例的增删改
    url(r'^create_webcase/$',create_webcase_views),
    url(r'^del_webcase/$',delete_webcase_views),
    url(r'^update_webcase/$',update_webcase_views),
    #导入功能测试用例
    url(r'^import_webcase/$',import_webcase_views),


    #----------------------webAuto url-----------------------------
    #自动化UI测试列表
    url(r'^autolist/$',antolist_view),
    #自动化测试用例的增删改
    url(r'^create_autocase/$',create_autocase_views),
    url(r'^del_autocase/$', delete_autocase_views),
    url(r'^update_autocase/$', update_autocase_views),
    #执行自动化测试-生成测试报告
    url(r'^run_autocase/$',run_autocase_views),
    url(r'^TestReport/$',report_webcase_views),
    #自动化列表排序
    url(r'^autosort/$',autosort_views),
]