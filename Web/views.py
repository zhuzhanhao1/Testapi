from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

#zzh测试frame首页
@login_required
def web_index_views(request):
    return render(request, 'index.html')

#后台首页
@login_required
def web_welcome_views(request):
    return render(request, 'web_welcome.html')

#erms功能测试
@login_required
def web_functionalTest_views(request):
    a = request.GET.get("belong", "")
    b = request.GET.get("system","")
    return render(request, 'web_functionalTest.html', {"user": "朱占豪", "abq":a, "system":b})

#erms自动化UI测试
@login_required
def web_autoTest_views(request):
    a = request.GET.get("belong", "")
    b = request.GET.get("system", "")
    return render(request, 'web_autoTest.html',{"abq":a, "system":b})

#快速测试
@login_required
def web_quicktest_views(request):
    return render(request, 'web_quicktest.html')

#接口首页
@login_required
def web_apiindex_views(request):
    a = request.GET.get("belong","")
    b = request.GET.get("system","")
    return render(request, "web_apiindex.html", {"abq":a,"system":b})

#流程接口首页
@login_required
def web_process_views(request):
    a = request.GET.get("belong", "")
    b = request.GET.get("system", "")
    return render(request, 'web_process.html', {"abq":a,"system":b})

#个人信息页
@login_required
def web_info_views(request):
    return render(request, 'userInfo.html')

#友情链接
@login_required
def web_linklist_views(request):
    return render(request, 'linkList.html')

#测试网址
@login_required
def web_linktest_views(request):
    return render(request, 'linktest.html')




