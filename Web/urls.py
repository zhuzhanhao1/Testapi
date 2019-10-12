from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^web_index/$',web_index_views),
    url(r'^web_welcome/$',web_welcome_views),
    url(r'^web_apiindex/$',web_apiindex_views),
    url(r'^web_transferindex/$',web_transferindex_views),
    url(r'^web_quicktest/$',web_quicktest_views),
    url(r'^web_webindex/$',web_webindex_views),
    url(r'^web_info/$',web_info_views),
]