import requests,json
import logging
from dingtalkchatbot.chatbot import DingtalkChatbot

url = "https://oapi.dingtalk.com/robot/send?access_token=e1790ceab2bf195233dda1cc1063045f4af3c6838c120770e24a5b6e48455e48"
# 初始化机器人小丁
def send_image():
    xiaoding = DingtalkChatbot(url)
    # xiaoding.send_text(msg='没有返回错误，实属优秀！')
    xiaoding.send_image(pic_url='data:image/jpeg;base64,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')

def send_link():
    xiaoding = DingtalkChatbot(url)
    xiaoding.send_link(title='正在直播中...', text='2万把诸葛...', message_url='https://www.huya.com')

def send_ding(content,head=None):
    params = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {
            "atMobiles": [""],
            "isAtAll": False
        }
    }
    if head == "老张":
        params = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": ["15270833545"],
                "isAtAll": False
            }
        }
    elif head == "老刘":
        params = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": ["15279438039"],
                "isAtAll": False
            }
        }
    elif head == "老李":
        params = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": ["13157155198"],
                "isAtAll": False
            }
        }
    elif head == "老江":
        params = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": ["15073326435"],
                "isAtAll": False
            }
        }
    # print(params)
    # logging.debug(params)

    headers = {
        "Content-Type":"application/json"
    }

    f = requests.post(url, data=json.dumps(params), headers=headers)
    if f.status_code==200:
        return True
    else:
        return False

if __name__ == "__main__":
    send_ding("尊敬的钉钉用户您好，为保障群机器人使用体验，从2019年9月18日起，我们将对群机器人功能进行升级维护。9月18日零点后，当前的Webhook将失效。需要群主或者机器人创建者，在【电脑端钉钉】-右上角【…】-【智能群助手】，找到对应的自定义机器人，点击Webhook右侧的【重置】，然后拷贝重置后的Webhook，更新到对应的自定义机器人服务。请注意鉴权密钥和机器人代码务必要妥善保管，严防泄露，否则会对你的企业沟通和信息安全造成重大影响哦，给您带来的不便深表歉意，感谢您对钉钉的支持。")
    # send_image()