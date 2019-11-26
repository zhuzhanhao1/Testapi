import sys,os
currentUrl = os.path.dirname(__file__)
cur_path = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(cur_path)


import pymysql

class ConnDataBase:
    def __init__(self,host="127.0.0.1",user='root',pwd='123456',
                 db='ERMS',port=3306,charset='utf8'):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = port
        self.charset = charset
        self.cursor = None
        self.connect = None

    def conn_base(self):
        try:
            self.connect = pymysql.connect(host=self.host,user=self.user,
                                           password=self.pwd,port=self.port,
                                           database=self.db,charset=self.charset)
        except:
            print("链接数据库失败")
            return False
        self.cursor = self.connect.cursor()
        return True

    def close_base(self):
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()
        return True

    def execute_sql(self,sql,params=None):
        '''执行sql'''
        if self.conn_base() == False:
            return False
        try:
            if self.connect and self.cursor:
                self.cursor.execute(sql,params)
                self.connect.commit()
        except:
            print("excute: "+sql+" error" )
            return False
        return True

    def fetchCount(self,sql,params=None):
        if self.conn_base() == False:
            return False
        self.execute_sql(sql,params)
        #返回操作数据库得到的一条结果数据
        return self.cursor.fetchone()
        # return self.cursor.fetchall()

    #根据用户身份获取用户的token
    def get_logininfo(self,identity):
        sql = "select username,password,url,token from ERMS.userinfo where identity='{}';".format(identity)
        res = self.fetchCount(sql)
        return res

    #获取所有的用户信息
    def get_logininfos(self):
        sql = "select * from ERMS.userinfo;"
        self.execute_sql(sql)
        return self.cursor.fetchall()

    #更具用户的身份更新用户的账号密码
    def update_logininfo(self,username,password,identity):
        sql = "update ERMS.userinfo set username='{zhanghao}',password='{mima}'  where identity='{shenfeng}';".format(zhanghao=username,mima=password,shenfeng=identity)
        print(sql)
        res = self.fetchCount(sql)
        return res

    #根据用户的身份更改用户的token
    def update_token(self,token,identity):
        sql = "update ERMS.userinfo set token='{token}' where identity='{shenfeng}';".format(token=token,shenfeng=identity)
        res = self.fetchCount(sql)
        return res

    #通过id获取接口参数的详细信息
    def get_requestParams(self,id):
        sql = "select parameterName,parameterThat,requestType,isMust,dataType from ERMS.requestParams where id={};".format(id)
        self.execute_sql(sql)
        return self.cursor.fetchall()

    #插入接口的详细信息
    def insert_requestParams(self,id,parameterName,parameterThat,requestType,isMust,dataType):
        sql = "insert into ERMS.requestParams (id,parameterName,parameterThat,requestType,isMust,dataType) values('{0}','{1}','{2}','{3}','{4}','{5}');".format(id,parameterName,parameterThat,requestType,isMust,dataType)
        res = self.fetchCount(sql)
        return res

if __name__ == "__main__":
    data = ConnDataBase()
    # print(data.update_logininfo("haoyi@amberdata.cn","Dctm@1234","admin"))
    # print(data.get_logininfo("sysadmin")[2])id
    # print(type(data.get_logininfo("sysadmin")[2]))
    # print(str(data.get_logininfo("sysadmin")[2],'utf-8'))
    # print(type(str(data.get_logininfo("sysadmin")[2],'utf-8')))
    # print(data.get_logininfo("admin"))
    # print(data.get_logininfo("uisysadmin"))
    # print(data.update_token("saffqewgwrguehrgo","ast"))
    # print(data.get_requestParams(2))
    # for i in data.get_requestParams(2):
    #     print(i[0])

    # print(data.insert_requestParams(123,"id","表单配置id","query","true","string"))
    # print(data.get_requestParams(203))
    # print(data.get_logininfos())
    for  i in data.get_logininfos():
        print(str(i[3],"utf-8"))
