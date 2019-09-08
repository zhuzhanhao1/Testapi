
# from steps.my_config import erms
import time
from selenium import webdriver
import os,sys

currentUrl = os.path.dirname(__file__)
cur_path = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(cur_path)

from .conn_database import ConnDataBase
from .my_base import Base

erms = {"url":"http://amberdata.cn/erms/v2"}

class Login(Base):
    uname = ("css selector", "[name='username']")
    pwd = ("css selector", "[name='password']")
    button = ("id", "goLogin")

    def get_info(self,data):
        db = ConnDataBase()
        return db.get_logininfo(data)

    def login(self,flag='sysadmin'):
        self.driver.get(erms["url"])
        if flag == "sysadmin":
            a = self.get_info(flag)
            self.clear(self.uname)
            self.sendKeys(self.uname,a[0])
            self.sendKeys(self.pwd,a[1])
            self.click(self.button)
            time.sleep(1)

        elif flag == "admin":
            b = self.get_info(flag)
            self.clear(self.uname)
            self.sendKeys(self.uname,b[0])
            self.clear(self.pwd)
            self.sendKeys(self.pwd,b[1])
            self.click(self.button)
            time.sleep(1)

        else:
            c = self.get_info(flag)
            self.clear(self.uname)
            self.sendKeys(self.uname,c[0])
            self.clear(self.pwd)
            self.sendKeys(self.pwd,c[1])
            self.click(self.button)
            time.sleep(1)


if __name__ == "__main__":
    d = webdriver.Chrome()
    a= Login(d)
    a.login("sysadmin")
