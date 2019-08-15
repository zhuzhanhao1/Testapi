import json

from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.keys import Keys
import sys
import os
currentUrl = os.path.dirname(__file__)
cur_path = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(cur_path)
from .my_base import Base
from .sysadmin_conf import *
from .login import Login
from .conn_db import ConnDataBase


class SystemManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        Login(cls.driver).login()
        cls.d = Base(cls.driver)
        cls.data = ConnDataBase()
        # cls.d.js_element(LoginDisplay)
        # time.sleep(3)
        # cls.d.js_accept()


    def tearDown(self):
        self.driver.refresh()

    @classmethod
    def tearDownClass(cls):
        cls.driver.delete_all_cookies()
        cls.driver.quit()

    def alert(self,data,times=1):
        self.d.js_element(data)
        time.sleep(times)
        self.d.js_accept()

    #匹配关键字
    def matching(self,a,b,c):
        try:
            eles = self.driver.find_elements_by_xpath(a)
            for ele in eles:
                alas = ele.find_element_by_xpath(b)
                if alas.text == c:
                    ele.click()
                    break
        except:
            print("请在仔细核对你所匹配的关键字是否存在")


    def test_a_unit_create(self):
        """入驻单位管理-新建入驻单位"""
        d = self.d
        d.click(unitmodel)              #点击入驻单位模块
        time.sleep(2)
        self.alert(CreateUnit)          #显示alert弹框
        self.d.js_element("document.getElementsByClassName('mat-flat-button mat-primary')[0].style.color='red'")
        d.click(unit_create_but)        #点击新建入驻单位
        time.sleep(1)

        result = json.dumps(eval(self.data.get_logininfo(3)[0]),ensure_ascii=False)  #从数据库获取数据，转换为字典取值
        print(result)
        print(type(result))
        jgdm_value = json.loads(result)["jgdm"]
        dwmc_value = json.loads(result)["dwmc"]
        qzh_value= json.loads(result)["qzh"]
        dwfzr_value = json.loads(result)["dwfzr"]
        bmmc_value = json.loads(result)["bmmc"]
        xm_value = json.loads(result)["xm"]
        mm_value = json.loads(result)["mm"]
        dzyj_value = json.loads(result)["dzyj"]


        d.sendKeys(jgdm,jgdm_value)     #输入机构代码
        time.sleep(1)
        d.sendKeys(dwmc,dwmc_value)     #输入单位名称
        time.sleep(1)
        d.sendKeys(qzh,qzh_value)       #输入全宗号
        time.sleep(1)
        d.sendKeys(dwfzr,dwfzr_value)   #输入单位负责人
        time.sleep(2)
        d.js_element(manager_info)      #进去管理员信息界面
        time.sleep(1)
        self.alert(CreateUnitManager)   #显示alert弹框
        d.sendKeys(bmmc,bmmc_value)     #输入部门名称
        time.sleep(1)
        d.sendKeys(xm,xm_value)         #输入姓名
        time.sleep(1)
        d.sendKeys(mm,mm_value)         #输入密码
        time.sleep(1)
        d.sendKeys(dzyj,dzyj_value)     #输入电子邮件
        time.sleep(1)
        d.js_element(cunit_determine)   #点击确定
        time.sleep(60)


    def test_b_unit_update(self):
        '''入驻单位管理-编辑入驻单位'''
        d = self.d
        d.click(unitmodel)              #点击入驻单位模块
        time.sleep(1)
        self.alert(UpdateUnit)          #显示alert弹框

        result = json.dumps(eval(self.data.get_logininfo(4)[0]),ensure_ascii=False)  #从数据库获取数据，转换为字典取值
        print(result)
        print(type(result))
        qzh_value = json.loads(result)["qzh"]
        print(qzh_value)
        lxdh_value = json.loads(result)['lxdh']

        self.matching(editor,unitname,qzh_value)   #匹配单位名字为"ONEPIECE"的做编辑操作
        time.sleep(2)
        d.clear(lxdh)
        d.sendKeys(lxdh,lxdh_value)     #输入联系方式
        # d.sendKeys(lxdh, Keys.BACK_SPACE)
        d.sendKeys(lxdh,Keys.ENTER)
        # d.submit(lxdh)                  #提交表单
        time.sleep(5)


    def test_c_unit_delete(self):
        '''入驻单位管理-删除入驻单位'''
        d = self.d
        d.click(unitmodel)              #点击入驻单位模块
        time.sleep(1)
        self.alert(DeleteUnit)          #显示alert弹框

        result = json.dumps(eval(self.data.get_logininfo(5)[0]),ensure_ascii=False)  #从数据库获取数据，转换为字典取值
        print(result)
        print(type(result))
        qzh_value = json.loads(result)["qzh"]

        self.matching(delete,unitname,qzh_value)  #匹配单位名字为"ONEPIECE"的做编辑操作
        time.sleep(2)
        d.js_element(dunit_determine)
        time.sleep(3)



    def test_d_policy_create(self):
        '''保留处置策略-新建保留处置策略'''
        d = self.d
        d.click(policymodel)                   #进入到保留处置策略模块
        time.sleep(1)
        self.alert(CreatePolicy)               #显示alert弹框

        d.js_element(policy_create)                 #点击新建按钮
        time.sleep(1)
        d.sendKeys(policy_year,Keys.BACK_SPACE)#退格

        result = json.dumps(eval(self.data.get_logininfo(6)[0]),ensure_ascii=False)  #从数据库获取数据，转换为字典取值
        print(result)
        print(type(result))
        year = json.loads(result)["year"]
        print(year)
        strategy = json.loads(result)["strategy"]
        month = json.loads(result)["month"]
        day = json.loads(result)["day"]

        d.sendKeys(policy_year,year)              #选择保留期限的年限xxx年
        time.sleep(1)
        d.click(choose_way)                    #下拉框选择(默认移交)
        d.js_element('$(".mat-option-text")[{}].click()'.format(strategy))                #选择销毁
        time.sleep(1)
        d.js_element(choose_month)             #下拉框选择-月
        time.sleep(1)
        d.js_element('$(".mat-option-text")[{}].click()'.format(month))                    #点击选中的月份
        time.sleep(1)
        d.js_element(choose_day)               #下拉框选择-日
        time.sleep(1)
        d.js_element('$(".mat-option-text")[{}].click()'.format(day))                      #点击选中的日期
        time.sleep(1)
        d.js_element(cpolicy_determine)        #点击确定
        time.sleep(5)


    def test_e_policy_update(self):
        '''保留处置策略-编辑保留处置策略'''
        d = self.d
        d.click(policymodel)                    #进入到保留处置策略模块
        time.sleep(1)
        self.alert(UpdatePolicy)                #显示alert弹框

        result = json.dumps(eval(self.data.get_logininfo(7)[0]),ensure_ascii=False)  #从数据库获取数据，转换为字典取值
        print(result)
        print(type(result))
        updatepolicy = json.loads(result)["updatepolicy"]
        strategy = json.loads(result)["strategy"]
        self.matching(editor,policyname,updatepolicy)  #匹配保留处置策略名字为"updatepolicy"的做编辑操作

        d.click(choose_way)                     #点击选择销毁或是移交方式
        time.sleep(1)
        d.js_element('$(".mat-option-text")[{}].click()'.format(strategy))                 #选择移交
        time.sleep(1)
        d.js_element(upolicy_determine)         #点击确定
        time.sleep(2)


    def test_f_policy_delete(self):
        '''保留处置策略-删除保留处置策略'''
        d = self.d
        d.click(policymodel)                    #进入到保留处置策略模块
        time.sleep(1)
        self.alert(DeletePolicy)                #显示alert弹框

        result = json.dumps(eval(self.data.get_logininfo(8)[0]),ensure_ascii=False)  #从数据库获取数据，转换为字典取值
        print(result)
        print(type(result))
        deletepolicy = json.loads(result)["deletepolicy"]

        self.matching(delete,policyname,deletepolicy)   #匹配保留处置策略名字为"deletepolicy"的做删除操作
        time.sleep(1)
        d.js_element(dpolicy_determine)         #点击确定
        time.sleep(2)


    @unittest.skip("")
    def test_source_create(self):
        '''档案来源设置-新建档案来源'''
        d = self.d
        d.click(sourcemodel)                        #进入到档案来源模块
        time.sleep(1)
        self.alert(CreateSource)                    #显示alert弹框
        d.js_element(source_create)                 #点击添加档案来源按钮
        time.sleep(2)
        d.sendKeys(source_name,source_name_value)   #输入档案来源的名称
        time.sleep(2)
        d.click(csource_determine)                  #点击确定
        time.sleep(1)


    @unittest.skip("")
    def test_source_update(self):
        '''档案来源设置-更新档案来源'''
        d = self.d
        d.click(sourcemodel)            #进入到档案来源模块
        time.sleep(1)
        self.alert(UpdateSource)        #显示alert弹框
        self.matching("","","")
        time.sleep(1)


    @unittest.skip("")
    def test_source_delete(self):
        '''档案来源设置-删除档案来源'''
        d = self.d
        d.click(sourcemodel)            #进入到档案来源模块
        time.sleep(1)
        self.alert(DeleteSource)        #显示alert弹框
        self.matching("","","")
        time.sleep(1)


    def test_a_forms_create(self):
        '''数据表单设置-新建数据表单'''
        d = self.d
        d.click(formsmodel)            #进入到数据表单模块
        time.sleep(1)
        self.alert(CreateForms)        #显示alert弹框
        d.js_element(forms_create)     #点击新建数据表单按钮
        time.sleep(1)

        result = json.dumps(eval(self.data.get_logininfo(1)[0]),ensure_ascii=False)  #从数据库获取数据，转换为字典取值
        print(result)
        print(type(result))
        formsname = json.loads(result)["forms_name"]
        time.sleep(1)

        d.sendKeys(bdmc,formsname)    #输入表单名称
        time.sleep(1)
        d.js_element(ysjfa)            #点击元数据方案选择按钮
        time.sleep(1)
        d.js_element(ysjfa_value)      #选择元数据方案的值
        time.sleep(1)
        d.submit(bdmc)                 #提交表单
        time.sleep(5)


    def test_a_forms_delete(self):
        '''数据表单设置-删除数据表单'''
        d = self.d
        d.click(formsmodel)            #进入到数据表单模块
        time.sleep(1)
        self.alert(DeleteForms)        #显示alert弹框

        result = json.dumps(eval(self.data.get_logininfo(1)[0]),ensure_ascii=False)  #从数据库获取数据，转换为字典取值
        print(result)
        print(type(result))
        formsname = json.loads(result)["forms_name"]
        time.sleep(1)

        self.matching(editor,formname,formsname)  #匹配数据表单名字为formsname的做编辑操作
        time.sleep(1)
        d.js_element(dformsdetermine)   #点击确定
        time.sleep(5)

    def test_view_create(self):
        '''视图管理-新建视图'''
        pass

    def test_view_update(self):
        '''视图管理-新建视图'''
        pass

    def test_view_delete(self):
        '''视图管理-新建视图'''
        pass


if __name__ == "__main__":
    unittest.main()

