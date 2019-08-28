from django.conf.urls import url

from .view_process import *
from .views import *
from .view_web import *
from .view_api import *

urlpatterns = [
    url(r'^login/$',login_views),
    url(r'^registered/$',registered_views),
    url(r'^welcome/$',welcome_views),

#----------------------Api url-----------------------------
    url(r'^index/$',index_views),
    url(r'^create_case/$',create_case_views),
    url(r'^import_case/$',import_case_views),
    url(r'^caselist/$',caselist_views),
    url(r'^search_name/$',search_name_views),
    url(r'^delete_case/$',delete_case_views),
    url(r'^update_case/$',update_case_views),
    url(r'^run_case/$',run_case_views),
    url(r'^logout/$',logout_views),
    url(r'^webindex/$',webindex_views),


#----------------------Api_v2 url-----------------------------
    url(r'^apiindex/$', apiindex_view),
    url(r'^apilist/$', apilist_view),
    url(r'^create_apicase/$', create_apicase_views),
    url(r'^del_apicase/$', delete_apicase_views),
    url(r'^update_apicase/$', update_apicase_views),
    url(r'^run_apicase/$', run_apicase_views),
    url(r'^update_token_api/$',update_token_api_views),

#----------------------Api_process  url-----------------------------
    url(r'^ProcessIndex/$', process_interface_view),
    url(r'^processlist/$', processlist_view),
    url(r'^create_processcase/$', create_processcase_views),
    url(r'^del_processcase/$', delete_processcase_views),
    url(r'^update_processcase/$', update_processcase_views),
    url(r'^run_processcase/$', run_processcase_views),
    url(r'^get_tokeninfo/$',get_tokeninfo_views),
    url(r'^update_token/$',update_token_views),
    url(r'^timetask/$',timetask_views),

    #----------------------web url-----------------------------
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
    url(r'^del_webcase/$',delete_autocase_views),
    url(r'^update_autocase/$',update_autocase_views),
    url(r'^update_dataready/$',update_dataready_views),
    url(r'^update_userinfo/$',update_userinfo_views),
    url(r'^get_userinfo/$',get_userinfo_views),
    url(r'^update_userinfo_api/$',update_userinfo_api_views),
    url(r'^detail',detail_views),


    #----------------------timing url-----------------------------
    url(r'^timing/$',timing_views),
    url(r'^performance/$',performance_views),

]