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
from .ast_conf import *
from .login import Login

class AstManagement(unittest.TestCase):
    '''档案员操作'''
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        Login(cls.driver).login(flag='ast')
        cls.d = Base(cls.driver)
        cls.d.move_to_element(mouse)            #鼠标移动悬浮
        time.sleep(1)
        cls.d.click(ywsd)                       #点击业务设定
        time.sleep(1)
        cls.d.js_element(LoginDisplay)
        time.sleep(3)
        cls.d.js_accept()

    # def setUp(self):
        # Login(self.driver).login()

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
    def bianji(self,a,b,c):
        try:
            eles = self.driver.find_elements_by_xpath(a)
            for ele in eles:
                alas = ele.find_element_by_xpath(b)
                print(alas.text)
                if alas.text == c and ele.get_attribute("title") == '编辑':
                    ele.click()
                    break
        except:
            print("请在仔细核对你所匹配的关键字是否存在")

    def shanchu(self,a,b,c):
        try:
            eles = self.driver.find_elements_by_xpath(a)
            for ele in eles:
                alas = ele.find_element_by_xpath(b)
                print(alas.text)
                if alas.text == c and ele.get_attribute("title") == '删除':
                    ele.click()
                    break
        except:
            print("请在仔细核对你所匹配的关键字是否存在")

#-------------------------------------------------------------------------#
    def test_aa_cate_create(self):
        '''类目保管期限设定模块-新建档案门类'''
        d = self.d
        d.click(lmbgqxsd)                   #进入类目保管期限模块
        self.alert(CreateCate)              #显示alert弹框
        d.js_element(create)                #点击新建档案门类
        time.sleep(1)

    def test_ab_cate_update(self):
        '''类目保管期限设定模块-编辑档案门类'''
        d = self.d
        d.click(lmbgqxsd)                   #进入类目保管期限模块
        self.alert(UpdateCate)              #显示alert弹框


    def test_ac_cate_delete(self):
        '''类目保管期限设定模块-删除档案门类'''
        d = self.d
        d.click(lmbgqxsd)                   #进入类目保管期限模块
        self.alert(DeleteCate)              #显示alert弹框

#-------------------------------------------------------------------------#
    def test_ba_custom_create(self):
        '''档案类型自定义模块-添加文件种类'''
        d = self.d
        time.sleep(1)
        d.click(dglxzdy)                    #进入到档案类型自定义模块
        self.alert(CreateCustom)            #显示alert弹框
        d.js_element(create)                #添加文件种类
        time.sleep(1)

    def test_bb_custom_update(self):
        '''档案类型自定义模块-编辑文件种类'''
        d = self.d
        time.sleep(1)
        d.click(dglxzdy)                    #进入到档案类型自定义模块
        self.alert(UpdateCustom)            #显示alert弹框

    def test_bc_custom_delete(self):
        '''档案类型自定义模块-删除文件种类'''
        d = self.d
        time.sleep(1)
        d.click(dglxzdy)                    #进入到档案类型自定义模块
        self.alert(DeleteCustom)            #显示alert弹框

#-------------------------------------------------------------------------#
    def test_ca_access_create(self):
        '''访问控制策略模块-新建访问控制策略'''
        d = self.d
        d.click(fwkzcl)                     #进入到访问控制策略模块
        self.alert(UpdateAccess)            #显示alert弹框
        d.js_element(create)
        time.sleep(1)
        d.sendKeys(clmc,clmc_value)         #输入策略名称
        time.sleep(1)
        d.sendKeys(msxx,msxx_value)         #输入描述信息
        time.sleep(1)
        d.js_element(azzjg)                 #点击按组织架构
        time.sleep(1)
        d.js_element(choose_zzjg)           #选择组织架构的部门
        time.sleep(1)
        d.js_element(choose_power)          #点击选择权限按钮
        time.sleep(1)
        d.js_element(power)                 #确定权限
        time.sleep(1)
        d.js_element(caccess_determine)     #点击确定创建的按钮
        time.sleep(2)



    def test_cb_access_update(self):
        '''访问控制策略模块-编辑访问控制策略'''
        d = self.d
        d.click(fwkzcl)                #进入到访问控制策略模块
        self.alert(UpdateAccess)            #显示alert弹框
        self.bianji(editor,accessname,"梅里号删除")
        time.sleep(2)
        d.sendKeys(msxx,Keys.BACK_SPACE)         #输入策略名称
        time.sleep(1)
        d.js_element(uaccess_determine)
        time.sleep(2)



    def test_cc_access_delete(self):
        '''访问控制策略模块-删除访问控制策略'''
        d = self.d
        d.click(fwkzcl)                #进入到访问控制策略模块
        self.alert(DeleteAccess)            #显示alert弹框
        self.shanchu(editor,accessname,"梅里号删除")
        time.sleep(1)
        d.js_element(daccess_determine)
        time.sleep(2)

#-------------------------------------------------------------------------#
    def test_da_policy_create(self):
        '''保留处置策略模块-新建保留处置策略'''
        d = self.d
        d.click(blczcl)                     #进入到保留处置策略模块
        self.alert(CreatePolicy)            #显示alert弹框
        d.js_element(create)                #新建保留处置策略
        time.sleep(2)
        d.sendKeys(policy_year,Keys.BACK_SPACE)#退格
        d.sendKeys(policy_year,4)              #选择保留期限的年限xxx年
        time.sleep(1)
        d.click(choose_way)                     #下拉框选择(默认移交)
        d.js_element(policy_xh)                #选择销毁
        time.sleep(2)
        d.js_element(choose_month)             #下拉框选择-月
        time.sleep(2)
        d.js_element(month)                    #点击选中的月份
        time.sleep(2)
        d.js_element(choose_day)               #下拉框选择-日
        time.sleep(2)
        d.js_element(day)                      #点击选中的日期
        time.sleep(2)
        d.js_element(cpolicy_determine)        #点击确定
        time.sleep(1)

    def test_db_policy_update(self):
        '''保留处置策略模块-编辑保留处置策略'''
        d = self.d
        d.click(blczcl)                     #进入到保留处置策略模块
        self.alert(UpdatePolicy)            #显示alert弹框
        self.bianji(editor,policyname,"保留4年后销毁")  #匹配保留处置策略名字为"保留4年后销毁"的做编辑操作
        d.click(choose_way)                     #点击选择销毁或是移交方式
        time.sleep(1)
        d.js_element(policy_yj)                 #选择移交
        time.sleep(2)
        d.js_element(upolicy_determine)         #点击确定
        time.sleep(2)


    def test_dc_policy_delete(self):
        '''保留处置策略模块-删除保留处置策略'''
        d = self.d
        d.click(blczcl)                     #进入到保留处置策略模块
        self.alert(DeletePolicy)            #显示alert弹框
        self.shanchu(editor,policyname,"保留4年后销毁")   #匹配保留处置策略名字为"保留4年后销毁"的做删除操作
        time.sleep(1)
        d.js_element(dpolicy_determine)         #点击确定
        time.sleep(1)

#-------------------------------------------------------------------------#
    def test_ea_source_create(self):
        '''档案来源设置模块-添加档案来源'''
        d = self.d
        d.click(dalysz)                     #进入到档案来源设置模块
        self.alert(CreateSource)            #显示alert弹框
        d.js_element(create)                #添加档案来源
        time.sleep(2)
        d.sendKeys(lymc,lymc_value)
        time.sleep(1)
        d.js_element(csource_determine)
        time.sleep(2)

    def test_eb_source_update(self):
        '''档案来源设置模块-编辑档案来源'''
        d = self.d
        d.click(dalysz)                     #进入到档案来源设置模块
        self.alert(UpdateSource)            #显示alert弹框
        self.bianji(editor,sourcename,"猪猪侠")
        time.sleep(1)
        d.sendKeys(lymc, "1")
        time.sleep(2)
        d.js_element(usource_determine)
        time.sleep(2)


    def test_ec_source_delete(self):
        '''档案来源设置模块-删除档案来源'''
        d = self.d
        d.click(dalysz)                     #进入到档案来源设置模块
        self.alert(DeleteSource)            #显示alert弹框
        self.shanchu(editor,sourcename,"猪猪侠1")
        time.sleep(2)
        d.js_element(dsource_determine)
        time.sleep(2)


#-------------------------------------------------------------------------#
    def test_fa_view_create(self):
        '''视图自定义模块-添加视图'''
        d = self.d
        d.click(stzdy)                      #进入到视图自定义模块
        self.alert(CreateView)              #显示alert弹框
        d.js_element(create)                #添加视图
        time.sleep(2)

    def test_fb_view_update(self):
        '''视图自定义模块-编辑视图'''
        d = self.d
        d.click(stzdy)                      #进入到视图自定义模块
        self.alert(UpdateView)              #显示alert弹框

    def test_fc_view_delete(self):
        '''视图自定义模块-删除视图'''
        d = self.d
        d.click(stzdy)                      #进入到视图自定义模块
        self.alert(DeleteView)              #显示alert弹框



if __name__ == "__main__":
    unittest.main()

