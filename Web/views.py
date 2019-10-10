from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

def web_index_views(request):
    return render(request, 'index.html')

def web_welcome_views(request):
    return render(request, 'web_welcome.html')


def web_apiindex_views(request):
    a = request.GET.get("belong","")
    return render(request,"web_apiindex.html",{"user":"朱占豪","abq":a})

def web_transferindex_views(request):
    a = request.GET.get("belong","")
    return render(request,"web_transferindex.html",{"user":"朱占豪","abq":a})
