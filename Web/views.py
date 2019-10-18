from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

@login_required
def web_index_views(request):
    return render(request, 'index.html')

@login_required
def web_welcome_views(request):
    return render(request, 'web_welcome.html')

@login_required
def web_functionalTest_views(request):
    a = request.GET.get("belong", "")
    return render(request, 'web_functionalTest.html', {"user": "朱占豪", "abq":a})

@login_required
def web_functionalTest_transfer_views(request):
    a = request.GET.get("belong", "")
    return render(request, 'web_functionalTest_transfer.html', {"user": "朱占豪", "abq":a})

def web_autoTest_views(request):
    return render(request, 'web_autoTest.html')

@login_required
def web_quicktest_views(request):
    return render(request, 'web_quicktest.html')

@login_required
def web_apiindex_views(request):
    a = request.GET.get("belong","")
    return render(request, "web_apiindex.html", {"user": "朱占豪", "abq":a})

@login_required
def web_transferindex_views(request):
    a = request.GET.get("belong","")
    return render(request, "web_transferindex.html", {"user": "朱占豪", "abq":a})

@login_required
def web_info_views(request):
    return render(request, 'userInfo.html')

@login_required
def web_linklist_views(request):
    return render(request, 'linkList.html')

@login_required
def web_linktest_views(request):
    return render(request, 'linktest.html')


