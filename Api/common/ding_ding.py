import requests,json
import logging
from dingtalkchatbot.chatbot import DingtalkChatbot
url = "https://oapi.dingtalk.com/robot/send?access_token=99c9913b6f5370541f17d56b3e1e32ca4d534b25f17df9fcedf44aa5173968a6"
# url = "https://oapi.dingtalk.com/robot/send?access_token=21829afa1afbefb42c38dfe171a4f6398448eec4da63bb914310067d22b256fc"
# 初始化机器人小丁
def send_image():
    xiaoding = DingtalkChatbot(url)
    # xiaoding.send_text(msg='没有返回错误，实属优秀！')
    xiaoding.send_image(pic_url='https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/u=1147110391,1099568746&fm=173&app=25&f=JPEG?w=640&h=640&s=4BA43A625AFA7BAF7D302CC60000A0A1')

def send_link(id,text):
    xiaoding = DingtalkChatbot(url)
    xiaoding.send_link(title='接口详情', text='{}请点击我......'.format(text), message_url='http://47.98.56.102:8000/detail_api/?id={}'.format(id))

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
    # pass
    send_link(1,'{李建构吃屎')
    # send_image()