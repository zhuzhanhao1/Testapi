import requests,json

#https://oapi.dingtalk.com/robot/send?access_token=092883f25a8da9b1b8d36b618980e48b92a14f2330facf487a55d74950587319
#"15270833545"
def send_ding(content):
    url = "https://oapi.dingtalk.com/robot/send?access_token=eec7d2777756d5cfb66f8f0f3f055946e09923f86796cf3186f6d02d0a66f940"
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
    headers = {
        "Content-Type":"application/json"
    }
    f = requests.post(url, data=json.dumps(params), headers=headers)
    if f.status_code==200:
        return True
    else:
        return False

if __name__ == "__main__":
    send_ding("一会吃啥")
