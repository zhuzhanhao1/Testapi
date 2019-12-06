#鼠标移动
mouse = ("id","snav")
mouse_out = ("css selector",".right--content--option--box")
#所有新建按钮统一标准
create = '$("button.mat-flat-button.mat-primary").click()'

#左侧动态模块选择
ywsd = ("xpath","//a[@class='ng-star-inserted' and @href='#/businessSet']")
#ywsd = ("css selector","a.ng-star-inserted[@href='#/businessSet']")

#档案类型自定义
dglxzdy = ("xpath","//span[text()='档案类型自定义']/..")


#类目保管期限设定
lmbgqxsd = ("xpath","//span[text()='类目保管期限设定']/..")


#保留处置策略管理
blczcl =("xpath","//span[text()='保留处置策略管理']/..")
#新建
policymodel = ("xpath","//span[text()='保留处置策略管理']/..")
policy_create = ("xpath", "//button[@class='mat-flat-button mat-primary']")
policy_year = ("xpath","//span[text()='年后']/../input")
choose_way= ("xpath", "//div[@class='mat-select-trigger'][1]")
policy_xh = '$(".mat-option-text")[1].click()'
choose_month = '$(".mat-select-trigger")[1].click()'
month = "$('#mat-option-5').click()"
choose_day = '$(".mat-select-trigger")[2].click()'
day = "$('#mat-option-22').click()"
cpolicy_determine = "$('.mat-flat-button.mat-primary')[1].click()"
#更新删除
policy_yj = '$(".mat-option-text")[0].click()'
upolicy_determine = "$('.mat-flat-button.mat-primary')[1].click()"
dpolicy_determine = '$(".swal2-confirm.swal2-styled").click()'


#访问控制策略管理
fwkzcl =("xpath","//span[text()='访问控制策略管理']/..")
#新增
clmc = ("id", "displayName")
clmc_value = "梅里号删除"
msxx = ("id", "description")
msxx_value = "测试访问控制策略"
azzjg = '$(".choose-caret").children()[0].click()'
choose_zzjg = '$(".everyuser-username")[0].click()'
choose_power = '$(".mat-select-trigger").click()'
power = '$(".mat-option.ng-star-inserted")[4].click()'
caccess_determine = '$(".mat-flat-button.mat-primary")[1].click()'
#编辑
uaccess_determine = "$('.mat-flat-button.mat-primary')[1].click()"
#删除
daccess_determine = '$(".swal2-confirm.swal2-styled").click()'



#档案来源设置
dalysz =("xpath","//span[text()='档案来源设置']/..")
lymc = ("xpath", "//div[@class='attribute--row--box__value']/input")
lymc_value = "猪猪侠"
csource_determine = '$("button.mat-flat-button.mat-primary")[1].click()'
#更新
usource_determine = '$("button.mat-flat-button.mat-primary")[1].click()'
#删除
dsource_determine = '$("button.swal2-confirm.swal2-styled").click()'


#视图自定义
stzdy = ("xpath","//span[text()='视图自定义']/..")

#匹配信息
formname = "../../../preceding-sibling::*[2]"
policyname = "../../../preceding-sibling::*[4]/span/div"
sourcename = "../../../preceding-sibling::*[2]/source-grid-name/span/span"
accessname = "../../../preceding-sibling::*[2]/span/div"
editor = "//span[@class='option--box']"
delete = "//span[@class='option--box ng-star-inserted']"


#alert
CreateCate ='alert("类目保管期限设定模块-新建档案门类")'
UpdateCate ='alert("类目保管期限设定模块-编辑档案门类")'
DeleteCate ='alert("类目保管期限设定模块-删除档案门类")'


CreateCustom = 'alert("档案类型自定义模块-添加文件种类")'
UpdateCustom = 'alert("档案类型自定义模块-编辑文件种类")'
DeleteCustom = 'alert("档案类型自定义模块-删除文件种类")'

CreateAccess = 'alert("访问控制策略模块-新建访问控制策略")'
UpdateAccess = 'alert("访问控制策略模块-编辑访问控制策略")'
DeleteAccess = 'alert("访问控制策略模块-删除访问控制策略")'

CreatePolicy = 'alert("保留处置策略模块-新建保留处置策略")'
UpdatePolicy = 'alert("保留处置策略模块-编辑保留处置策略")'
DeletePolicy = 'alert("保留处置策略模块-删除保留处置策略")'

CreateSource = 'alert("档案来源设置模块模块-添加档案来源")'
UpdateSource = 'alert("档案来源设置模块模块-编辑档案来源")'
DeleteSource = 'alert("档案来源设置模块模块-删除档案来源")'

CreateView = 'alert("视图自定义模块-新建视图")'
UpdateView = 'alert("视图自定义模块-编辑视图")'
DeleteView = 'alert("视图自定义模块-删除视图")'


LoginDisplay = 'alert("档案员登录，首先要做的就是业务设定，业务设定模块包括:类目保管期限设定，保留处置策略设定，档案类型自定义")'