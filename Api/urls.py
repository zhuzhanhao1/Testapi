from django.conf.urls import url
from .view_process import *
from .views import *
from .view_web import *
from .view_api import *

urlpatterns = [
    url(r'^login/$',login_views),
    url(r'^welcome/$',welcome_views),
    url(r'^logout/$',logout_views),
    # url(r'^import_case/$',import_case_views),
    url(r'^quickTest/$',quickTest_views),


#----------------------Api_v2 url-----------------------------
    url(r'^apiindex/$', apiindex_view),
    url(r'^apilist/$', apilist_view),

    url(r'^transferindex/$', transferindex_view),
    url(r'^transferlist/$', transferlist_view),

    url(r'^adminindex/$', adminindex_view),
    url(r'^adminlist/$', adminlist_view),

    url(r'^create_apicase/$', create_apicase_views),
    url(r'^del_apicase/$', delete_apicase_views),
    url(r'^update_apicase/$', update_apicase_views),
    url(r'^run_apicase/$', run_apicase_views),
    url(r'^update_token_api/$',update_token_api_views),
    url(r'^detail_api/$',detail_api_views),
    url(r'^export_data/$',export_data_views),
    url(r'^ding_ding/$',ding_ding_view),
    url(r'^field_apilist/$',field_apilist_views),


#----------------------Api_process  url-----------------------------
    url(r'^ProcessIndex/$', process_interface_view),
    url(r'^processlist/$', processlist_view),
    url(r'^create_processcase/$', create_processcase_views),
    url(r'^del_processcase/$', delete_processcase_views),
    url(r'^update_processcase/$', update_processcase_views),
    url(r'^run_processcase/$', run_processcase_views),
    url(r'^timetask/$',timetask_views),
    url(r'^detail/$',detail_views),
    url(r'^get_userinfo_transfer/$',get_userinfo_transfer_views),
    url(r'^export_data_process/$', export_data_process_views),


    #----------------------web url-----------------------------
    url(r'^webindex/$',webindex_views),
    url(r'^weblist/$',weblist_view),
    url(r'^run_webcase/$',run_webcase_views),
    url(r'^create_webcase/$',create_webcase_views),
    url(r'^del_webcase/$',delete_webcase_views),
    url(r'^update_webcase/$',update_webcase_views),
    url(r'^import_webcase/$',import_webcase_views),
    url(r'^TestReport/$',report_webcase_views),


    #----------------------webAuto url-----------------------------
    url(r'^autolist/$',antolist_view),
    url(r'^create_autocase/$',create_autocase_views),
    url(r'^run_autocase/$',run_autocase_views),
    url(r'^del_autocase/$',delete_autocase_views),
    url(r'^update_autocase/$',update_autocase_views),
    url(r'^update_dataready/$',update_dataready_views),
    url(r'^get_userinfo/$',get_userinfo_views),
    url(r'^update_userinfo_api/$',update_userinfo_api_views),


    #----------------------timing url-----------------------------
    url(r'^timing/$',timing_views),
    url(r'^performance/$',performance_views),

]