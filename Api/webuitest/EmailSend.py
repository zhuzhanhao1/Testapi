import os
cur_path = os.path.dirname(os.path.realpath(__file__))
cur_path1 = os.path.dirname(os.path.realpath(cur_path))
case_path = os.path.join(cur_path1, "report/TestReport.html")

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendEmail:
    global send_user
    global email_host
    global password
    password = "onhqpokaljtmbbfb"
    email_host = "smtp.qq.com"
    send_user = "971567069@qq.com"


    def send_mail(self,user_list,sub,content):
        user = "朱占豪" + "<" + send_user + ">"
        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['Subject'] = sub
        message['From'] = user
        message['To'] = ";".join(user_list)
        # 邮件正文内容
        message.attach(MIMEText(content, 'plain', 'utf-8'))
        # 构造附件（附件为txt格式的文本）
        att = MIMEText(open(case_path, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = 'attachment; filename="TestReport.html"'
        message.attach(att)
        server = smtplib.SMTP_SSL()
        server.connect(email_host,465)# 启用SSL发信, 端口一般是465
        server.login(send_user,password)
        server.sendmail(user,user_list,message.as_string())
        server.close()

    def send_main(self,content):
        user_list = ['531969094@qq.com']
        sub = "ERMSv2-UI自动化测试报告"
        content = content
        self.send_mail(user_list,sub,content)


if __name__ == '__main__':
    send = SendEmail()
    send.send_main("lala")
