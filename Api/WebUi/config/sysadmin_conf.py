# 新建入驻单位
unitmodel = ("xpath","//span[text()='入驻单位管理']/..")
unit_create_but = ("xpath","//button[@class='mat-flat-button mat-primary']")
jgdm = ("id","code")
dwmc = ("id","displayName")
qzh = ("id","fonds")
dwfzr = ("id","officer")

#单位管理员信息
manager_info = '$("div.mat-tab-label.mat-ripple.ng-star-inserted").click()'
bmmc = ("id","deptDisplayName")
xm = ("id","userDisplayName")
mm = ("id","userPassword")
dzyj = ("id","userAddress")
cunit_determine = '$("button.mat-flat-button.mat-primary")[1].click()'

#编辑入驻单位
lxdh = ("id","telephone")
uunit_determine = '$("button.mat-flat-button.mat-primary")[1].click()'

#删除入驻单位
dunit_determine = '$("button.swal2-confirm.swal2-styled").click()'


#保管处置策略创建
policymodel = ("xpath","//span[text()='保留处置策略管理']/..")

# policy_create = ("xpath", "//button[@class='mat-flat-button mat-primary']")
policy_create = '$(".mat-flat-button.mat-primary")[0].click()'


policy_year = ("xpath","//span[text()='年后']/../input")
choose_way= ("xpath", "//div[@class='mat-select-trigger'][1]")

policy_xh = '$(".mat-option-text")[1].click()'
choose_month = '$(".mat-select-trigger")[1].click()'

month = "$('#mat-option-5').click()"
choose_day = '$(".mat-select-trigger")[2].click()'
day = "$('#mat-option-22').click()"
cpolicy_determine = "$('button.mat-flat-button.mat-primary')[1].click()"
#保管处置策略跟新、删除
policy_yj = '$(".mat-option-text")[0].click()'
upolicy_determine = "$('.mat-flat-button.mat-primary')[1].click()"
dpolicy_determine = '$(".swal2-confirm.swal2-styled").click()'


#档案来源创建
sourcemodel = ("xpath","//span[text()='档案来源设置']/..")
source_create = '$("button.mat-flat-button.mat-primary").click()'
source_name = ("xpath","//div[@class='attribute--row--box__value']/input")
source_name_value = "橡胶果实"
csource_determine = "$('.mat-flat-button.mat-primary')[1].click()"
#档案来源更新



#档案来源删除



#数据表单
formsmodel = ("xpath","//span[text()='数据表单设置']/..")
forms_create = "$('.mat-flat-button.mat-primary')[0].click()"
# bdmc = ("id","name")
bdmc = ("xpath","//input[@id='name']")
bdmc_value = "2019年检登记表单"
ysjfa = "$('.mat-select-trigger')[0].click()"
ysjfa_value = '$("#mat-option-2")[0].click()'
dformsdetermine = '$(".swal2-confirm.swal2-styled")[0].click()'


#视图管理





#匹配信息
formname = "../../../preceding-sibling::*[2]"
policyname = "../../../preceding-sibling::*[4]/span/div"
unitname = "../../../following-sibling::div[1]"
editor = "//span[@class='option--box']"
delete = "//span[@class='option--box ng-star-inserted']"


#alert
LoginDisplay = 'alert("系统管理员登录,首先要做的是创建入驻单位,主要模块有:入驻单位管理、保留处置策略管理、档案来源设置、数据表单设置、视图管理")'
CreateUnit = 'alert("入驻单位管理-新建入驻单位")'
CreateUnitManager = 'alert("此处创建一个单位管理员的账号")'
UpdateUnit = "alert('入驻单位管理-编辑入驻单位')"
DeleteUnit = 'alert("入驻单位管理-删除入驻单位,删除单位要谨慎")'
CreatePolicy = 'alert("保留处置策略-新建保留处置策略")'
UpdatePolicy = 'alert("保留处置策略-编辑保留处置策略")'
DeletePolicy = 'alert("保留处置策略-删除保留处置策略")'
CreateSource = 'alert("档案来源设置-新建档案来源")'
UpdateSource = 'alert("档案来源设置-更新档案来源")'
DeleteSource = 'alert("档案来源设置-删除档案来源")'
CreateForms = 'alert("数据表单设置-新建数据表单")'
DeleteForms = 'alert("数据表单设置-删除数据表单")'
CreateView = 'alert("视图管理-新建视图")'
UpdateView = 'alert("视图管理-更新视图")'
DeleteView = 'alert("视图管理-删除视图")'