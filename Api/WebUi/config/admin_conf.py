#基本信息
baseinfo_model = ("xpath","//span[text()='基本信息']/..")
base_update = '$("button.mat-flat-button.mat-primary")[0].click()'
base_update_determine = '$("button.mat-flat-button.mat-primary")[1].click()'

#部门管理
deptmanager_model = ("xpath","//span[text()='部门管理']/..")
create_dept = '$("button.mat-flat-button.mat-primary").click()'
bmmc = ("id","displayName")
bmmc_value = "梅里号"
bmxh = ("id","code")
bmxh_value = "02"

#编辑部门
cz = ("id","fax")
cz_value = "123456"

#删除部门
dept_delete_determine = '$(".swal2-confirm.swal2-styled")[0].click()'


#用户管理
usermanager_model = ("xpath","//span[text()='用户管理']/..")
#上传用户
load_user = '$("button.mat-flat-button.mat-primary")[0].click()'
load = ("xpath","//input[@class='mat-menu-item__button']")
path = "/Users/zhuzhanhao/Downloads/用户模板.xls"
load_determine = "$('.mat-flat-button.mat-primary')[2].click()"
load_cancel= "$('.mat-stroked-button')[6].click()"
#创建用户
create_user = '$("button.mat-flat-button.mat-primary")[1].click()'
yhm = ("id","displayName")
yhm_value = "索隆"
mm = ("id","password")
mm_value = "Dctm@1234"
yjdz = ("id","address")
yjdz_value = "suol@amberdata.cn"
ssbm = '$("div.mat-select-trigger")[3].click()'
ssbm_value = '$("mat-option.mat-option.ng-star-inserted")[0].click()'
js = '$("div.mat-select-trigger")[4].click()'
js_value = '$("mat-option.mat-option")[4].click()'
depthead = '$("input#departmentOfficer-input").click()'
xh = ("id","code")
xh_value = "02"
#编辑用户
dh = ("id","telephone")
dh_value = "123456"

#启动用户
freezelist = ("link text","冻结用户")
djyy = ("xpath", "//div[text()='冻结原因：']/following-sibling::textarea[1]")
djyy_value = "我长的不好看"
restorelist = ("link text","正常用户")
restore_determine = '$(".swal2-confirm.swal2-styled").click()'


#搜索
ajs = '$("div.mat-select-trigger")[0].click()'
ajs_value = '$("mat-option.mat-option.ng-star-inserted")[3].click()'
abm = '$("div.mat-select-trigger")[1].click()'
abm_value = '$("mat-option.mat-option.ng-star-inserted")[1].click()'
search = ("xpath","//div[@class='right--content--option--box']/div/input")
search_value = "路飞"
search_button = 'document.getElementsByClassName("search--btn mat-stroked-button")[0].click()'


#循环遍历所需名字
editor = "//span[@class='option--box']"
delete = "//span[@class='option--box ng-star-inserted']"
deptname = "../../../preceding-sibling::*[2]"
username = "../../../preceding-sibling::*[4]"


#alert
LoginDisplay = 'alert("单位管理员登录,主要职能是管理自己单位的人员。主要模块:单位基本信息、部门管理、用户管理")'
BaseInfo = 'alert("基本信息展示-编辑单位基本信息")'
CreateDept = 'alert("部门管理-创建部门")'
UpdateDept = 'alert("部门管理-编辑部门")'
DeleteDept = 'alert("部门管理-删除部门")'
CreateUser = 'alert("用户管理-创建用户")'
UpdateUser = 'alert("用户管理-编辑用户")'
FreezeUser= 'alert("用户管理-冻结用户")'
RestoreUser = 'alert("用户管理-启用用户")'
SearchUser = 'alert("用户管理-搜索")'
UploadUser = 'alert("用户管理-上传用户")'