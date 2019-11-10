from django.db import models

# Create your models here.
class User(models.Model):
    uphone = models.CharField(max_length=11,verbose_name="手机号码")
    upwd = models.CharField(max_length = 30,verbose_name="密码")
    uname = models.CharField(max_length = 20,verbose_name="用户名")
    uemail = models.EmailField(verbose_name="电子邮箱")
    isActive = models.BooleanField(default=True)


#单一API接口测试
class Case(models.Model):
    caseid = models.AutoField(primary_key=True,max_length=200,unique=True)
    casename = models.CharField(max_length=100,verbose_name="用例名称")
    identity = models.CharField(max_length=50,verbose_name="用户身份")
    url = models.CharField(max_length=250,verbose_name="访问路径")
    method = models.CharField(max_length = 20,verbose_name="请求方式")
    header = models.CharField(max_length=200,verbose_name="请求头")
    params = models.TextField(verbose_name="请求参数")
    body = models.TextField(verbose_name="请求体内容")
    exceptres = models.CharField(max_length=250,verbose_name="期望结果")
    result = models.TextField(verbose_name="执行结果")
    belong = models.CharField(max_length=50,verbose_name="所属模块")
    create_time = models.DateTimeField(auto_now=True,null=True)
    isprocess = models.CharField(max_length=50, verbose_name="是否为流程测试")
    # belong_system = models.CharField(max_length=60,verbose_name="所属系统")
    #python3 manage.py migrate Api --fake
    system = models.CharField(max_length=50, verbose_name="所属系统")
    sortid = models.IntegerField(verbose_name="排序号")

    def __str__(self):
        return self.casename


#流程API接口测试
class Processapi(models.Model):
    caseid = models.AutoField(primary_key=True,max_length=200,unique=True)
    casename = models.CharField(max_length=100,verbose_name="用例名称")
    identity = models.CharField(max_length=50,verbose_name="用户身份")
    url = models.CharField(max_length=250,verbose_name="访问路径")
    method = models.CharField(max_length = 20,verbose_name="请求方式")
    header = models.CharField(max_length=200,verbose_name="请求头")
    params = models.TextField(verbose_name="请求参数")
    body = models.TextField(verbose_name="请求体内容")
    exceptres = models.CharField(max_length=250,verbose_name="期望结果")
    result = models.TextField(verbose_name="执行结果")
    belong = models.CharField(max_length=50,verbose_name="所属模块")
    isprocess = models.CharField(max_length=20,verbose_name="是否有依赖")
    depend_id = models.CharField(max_length=20,verbose_name="依赖的caseID")
    depend_key = models.CharField(max_length=500,verbose_name="依赖的key")
    replace_key = models.CharField(max_length=500,verbose_name="替换的key")
    replace_position = models.CharField(max_length=50,verbose_name="替换的内容区域",default="params")
    order_no = models.CharField(verbose_name="排序号",max_length=20)
    sortid = models.IntegerField(verbose_name="排序号")
    system = models.CharField(max_length=50, verbose_name="所属系统")

    def __str__(self):
        return self.casename


# web自动化测试/功能测试
class Webcase(models.Model):
    webcaseid = models.AutoField(primary_key=True, max_length=200, unique=True)
    webbelong = models.CharField(verbose_name="父模块",max_length=250)
    webcase_models = models.CharField(verbose_name='所属模块', max_length=250)
    webfunpoint = models.CharField(verbose_name="功能点",max_length=250)
    webidentity = models.CharField(max_length=50, verbose_name="用户身份",blank=True)
    webcasename = models.CharField(verbose_name='测试用例名称', max_length=250)
    webteststep = models.TextField(verbose_name='测试步骤')
    webpremise = models.CharField(verbose_name="前提条件",max_length=500)
    webexceptres = models.CharField(max_length=500, verbose_name="期望结果")
    webresult = models.TextField(verbose_name="执行结果",blank=True)
    webcreat_time = models.DateTimeField(verbose_name='创建时间', auto_now=True,blank=True)
    system = models.CharField(max_length=50, verbose_name="所属系统")

    def __str__(self):
        return self.webcasename



#WebAuto测试
class Autocase(models.Model):
    autoid = models.AutoField(primary_key=True, max_length=200, unique=True)
    autobelong = models.CharField(verbose_name="父模块",max_length=250)
    autoidentity = models.CharField(max_length=50, verbose_name="用户身份",blank=True)
    autoname = models.CharField(verbose_name='测试用例名称', max_length=250)
    autostep = models.TextField(verbose_name='测试步骤')
    autodataready = models.CharField(verbose_name="数据准备",max_length=500)
    autoexceptres = models.CharField(max_length=500, verbose_name="期望结果")
    autoresult = models.TextField(verbose_name="执行结果",blank=True)
    autocreat_time = models.DateTimeField(verbose_name='创建时间', auto_now=True,blank=True)
    sortid = models.IntegerField(verbose_name="排序号")
    system = models.CharField(max_length=50, verbose_name="所属系统")


    def __str__(self):
        return self.autoname
