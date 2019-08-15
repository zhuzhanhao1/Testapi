import json

from selenium import webdriver
import unittest
import time
import sys
import os
from selenium.webdriver.common.keys import Keys
currentUrl = os.path.dirname(__file__)
cur_path = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(cur_path)
from .my_base import Base
from .admin_conf import *
from .login import Login
from .conn_db import ConnDataBase


class UnitManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        Login(cls.driver).login(flag='admin')
        cls.d = Base(cls.driver)
        cls.data = ConnDataBase()
        # cls.d.js_element(LoginDisplay)  #打开浏览器首先提示单位管理员登录的弹框
        # time.sleep(3)
        # cls.d.js_accept()

    def tearDown(self):
        # self.driver.delete_all_cookies()
        self.driver.refresh()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def alert(self,data,times=2):
        time.sleep(1)
        self.d.js_element(data)
        time.sleep(times)
        self.d.js_accept()

    #匹配关键字
    def matching(self,a,b,c):
        try:
            eles = self.driver.find_elements_by_xpath(a)
            for ele in eles:
                alas = ele.find_element_by_xpath(b)
                print(alas.text)
                if alas.text == c:
                    ele.click()
                    break
        except:
            print("请在仔细核对你所匹配的关键字是否存在")

    def test_a_baseinfo(self):
        """基本信息-展示-编辑单位基本信息"""
        d = self.d
        self.alert(BaseInfo)
        d.click(baseinfo_model)             #进去基本信息模块
        time.sleep(1)
        d.js_element(base_update)           #点击编辑信息
        time.sleep(1)
        d.sendKeys(dh,dh_value)         #输入电话号码
        time.sleep(1)
        d.js_element(base_update_determine) #点击确定
        time.sleep(2)


    def test_b_create_dept(self):
        '''部门管理-创建部门'''
        d = self.d
        d.click(deptmanager_model)          #进入到部门管理模块
        self.alert(CreateDept)              #提示alert弹框
        d.js_element(create_dept)           #点击创建部门
        time.sleep(1)
        try:
            result = json.dumps(eval(self.data.get_logininfo(9)[0]),ensure_ascii=False)  #从数据库获取数据，转换为字典取值
            print(result)
            print(type(result))
            dept_name = json.loads(result)["dept_name"]
            number = json.loads(result)["number"]
            d.sendKeys(bmmc, dept_name)  # 输入部门名称
            time.sleep(1)
            d.sendKeys(bmxh, number)  # 输入部门序号
            time.sleep(1)
            d.js_element(base_update_determine)  # 点击确定
            time.sleep(2)
        except:
            self.alert('alert("获取数据失败，请核对信息")')





    def test_c_update_dept(self):
        '''部门管理-编辑部门'''
        d = self.d
        d.click(deptmanager_model)      #进入到部门管理模块
        self.alert(UpdateDept)          #提示alert弹框

        result = json.dumps(eval(self.data.get_logininfo(10)[0]), ensure_ascii=False)  # 从数据库获取数据，转换为字典取值
        print(result)
        print(type(result))
        dept_name = json.loads(result)["dept_name"]
        fax = json.loads(result)["fax"]

        self.matching(editor,deptname,dept_name)   #匹配部门名字为梅里号的部门做编辑操作
        time.sleep(1)
        d.sendKeys(cz,fax)         #编辑输入框，输入传真信息
        time.sleep(1)
        d.submit(cz)                    #提交表单
        time.sleep(5)


    def test_d_delete_dept(self):
        '''部门管理-删除部门'''
        d = self.d
        d.click(deptmanager_model)          #进入到部门管理模块
        self.alert(DeleteDept)              #提示alert弹框

        result = json.dumps(eval(self.data.get_logininfo(11)[0]), ensure_ascii=False)  # 从数据库获取数据，转换为字典取值
        print(result)
        print(type(result))
        dept_name = json.loads(result)["dept_name"]


        self.matching(delete,deptname,dept_name)    #匹配名字为梅里号的部门做删除操作
        time.sleep(1)
        d.js_element(dept_delete_determine) #确定删除
        time.sleep(5)


    def test_e_user_create(self):
        '''用户管理-创建用户'''
        d = self.d
        d.click(usermanager_model)      #进入到用户管理模块
        self.alert(CreateUser)          #提示alert弹框
        d.js_element(create_user)       #点击创建用户按钮
        time.sleep(1)

        result = json.dumps(eval(self.data.get_logininfo(12)[0]), ensure_ascii=False)  # 从数据库获取数据，转换为字典取值
        print(result)
        print(type(result))
        user_name = json.loads(result)["user_name"]
        password = json.loads(result)["password"]
        email = json.loads(result)["email"]
        belong_dept = json.loads(result)["belong_dept"]
        role = json.loads(result)["role"]
        number = json.loads(result)["number"]
        depthead = json.loads(result)["depthead"]

        d.sendKeys(yhm,user_name)       #输入用户名
        time.sleep(1)
        d.sendKeys(mm,password)         #输入密码
        time.sleep(1)
        d.sendKeys(yjdz,email)     #输入邮件地址
        time.sleep(1)
        d.js_element(ssbm)              #点击所属部门
        time.sleep(1)
        d.js_element('$("mat-option.mat-option.ng-star-inserted")[{}].click()'.format(belong_dept))   #选择所属的部门
        time.sleep(1)
        d.js_element(js)                #点击角色
        time.sleep(1)
        d.js_element('$("mat-option.mat-option")[{}].click()'.format(role))          #选择角色
        time.sleep(1)
        if depthead == 'true':
            d.js_element(depthead)          #勾上为部门负责人
            time.sleep(1)

        d.sendKeys(xh,number)         #输入序号
        time.sleep(1)
        d.submit(xh)
        time.sleep(2)


    def test_j_user_upload(self):
        '''用户管理-上传用户'''
        d = self.d
        d.click(usermanager_model)      #进入到用户管理模块
        self.alert(UploadUser)          #提示alert弹框
        d.js_element(load_user)         #点击上传用户
        time.sleep(1)
        d.sendKeys(load,path)           #选择上传的文件
        time.sleep(1)
        d.js_element(load_determine)    #确定上传
        time.sleep(2)


    def test_f_user_update(self):
        '''用户管理-编辑用户'''
        d = self.d
        d.click(usermanager_model)      #进入到用户管理模块
        self.alert(UpdateUser)          #提示alert弹框
        self.matching(editor,username,"路飞")     #匹配名字为路飞的用户做编辑操作
        time.sleep(1)
        d.sendKeys(dh,dh_value)         #输入电话号码
        time.sleep(1)
        d.js_element(load_determine)    #点击确定按钮
        time.sleep(2)



    def test_g_user_freeze(self):
        '''用户管理-冻结用户'''
        d = self.d
        d.click(usermanager_model)      #进入到用户管理模块
        self.alert(FreezeUser)          #提示alert弹框
        self.matching(delete,username,"索隆")     #匹配名字为娜美的用户做冻结操作
        time.sleep(1)
        d.sendKeys(djyy,djyy_value)
        time.sleep(1)
        d.js_element(load_determine)    #点击确定按钮
        time.sleep(2)


    def test_h_user_restore(self):
        '''用户管理-启用用户'''
        d = self.d
        d.click(usermanager_model)           #进入到用户管理模块
        self.alert(RestoreUser)              #提示alert弹框
        d.click(freezelist)                  #点击进入冻结用户列表页
        time.sleep(1)
        self.matching(delete,username,"索隆") #匹配名字为娜美的用户做启用操作
        time.sleep(1)
        d.js_element(restore_determine)      #点击确定启用用户按钮
        time.sleep(2)


    def test_i_user_search(self):
        '''用户管理-搜索'''
        d = self.d
        d.click(usermanager_model)          #进入到用户管理模块
        d.click(restorelist)                #进入到用正常用户列表
        time.sleep(1)
        self.alert(SearchUser)              #提示alert弹框
        d.sendKeys(search,search_value)     #输入搜索内容
        time.sleep(1)
        d.js_element(search_button)         #点击搜索
        time.sleep(1)
        d.sendKeys(search,Keys.BACK_SPACE)  #删除搜索内容
        d.sendKeys(search, Keys.BACK_SPACE) #删除搜索内容
        time.sleep(1)
        d.js_element(search_button)         #点击搜索
        time.sleep(1)
        d.js_element(ajs)                   #按角色
        time.sleep(1)
        d.js_element(ajs_value)             #选择角色
        time.sleep(1)
        d.js_element(abm)                   #按部门
        time.sleep(1)
        d.js_element(abm_value)             #选择部门
        time.sleep(2)


if __name__ == "__main__":
    unittest.main()

