import json

import pymysql

class ConnDataBase:
    def __init__(self,host="127.0.0.1",user='root',pwd='123456',
                 db='Testapi',port=3306,charset='utf8'):
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


    def get_logininfo(self,id):
        sql = "select autodataready from Testapi.api_autocase where autoid='{}';".format(id)
        # res = self.fetchCount(sql)[0]
        # res_a = eval(res)
        self.execute_sql(sql)
        return self.cursor.fetchone()



if __name__ == "__main__":
    data = ConnDataBase()
    # result = data.get_logininfo(1)[0]
    # print(result)
    # print(type(result))
    # new_res = eval(result)
    data_a = data.get_logininfo(1)[0]
    data_b = json.dumps(eval(data_a),ensure_ascii=False)
    print(data_b)
    data_c = json.loads(data_b)
    print(data_c["forms_name"])
    print(type(data_c))
    print(data_a)
