import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.


# 用户登录
def login_views(request):
    if request.POST:
        username = password = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = auth.authenticate(username=username,password=password)  #认证给出的用户名和密码
        if user is not None and user.is_active:    #判断用户名和密码是否有效
            auth.login(request, user)
            request.session['user'] = username  #跨请求的保持user参数
            response = HttpResponseRedirect('/welcome/')
            return response
        else:
            messages.add_message(request, messages.WARNING, '账户或者密码错误，请检查')
            print('账户或者密码错误，请检查')
            return render(request, 'login.html')
    return render(request, 'login.html')


# 退出登录
@login_required
def logout_views(request):
    auth.logout(request)
    return render(request, 'login.html')

# 首页
@login_required
def welcome_views(request):
    return render(request, "welcome.html")


# 启动Jenkins服务
@login_required
def timing_views(request):
    os.system("java -jar /Users/zhuzhanhao/jenkins.war")
    return render(request, "welcome.html")

# 启动jmeter
@login_required
def performance_views(request):
    os.system("sh /Users/zhuzhanhao/apache-jmeter-5.1/bin/jmeter.sh")
    return render(request, "welcome.html")

# 快速测试
@login_required
def quicktest_views(request):
    return render(request, "quickTest.html")

#流程测试响应结果
@login_required
def process_result_views(request):
    return render(request,"process_result.html")





