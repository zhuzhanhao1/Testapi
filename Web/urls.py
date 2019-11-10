from django.conf.urls import url
from .views import *

urlpatterns = [
    #测试系统V2版首页
    url(r'^web_index/$',web_index_views),
    url(r'^web_welcome/$',web_welcome_views),
    #接口测试首页
    url(r'^web_apiindex/$',web_apiindex_views),
    #单一接口快速测试首页
    url(r'^web_quicktest/$',web_quicktest_views),
    #功能测试首页
    url(r'^web_functionalTest/$',web_functionalTest_views),
    #自动化UI测试首页
    url(r'^web_autoindex/$',web_autoTest_views),
    #个人信息首页
    url(r'^web_info/$',web_info_views),
    #友情链接首页
    url(r'^web_linklist/$',web_linklist_views),
    #测试网址首页
    url(r'^web_linktest/$',web_linktest_views),
    #流程接口测试首页
    url(r'^web_process/$',web_process_views),
]