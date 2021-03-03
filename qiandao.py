#!/usr/bin/python3
# -*- coding: utf-8 -*
# -----------------------------------

import requests
import json
from hashlib import md5
from time import sleep
import random
import time
import yagmail
import os


session = requests.Session()
phone = os.environ["PHONE"]  # 改成你的手机号
pwd = os.environ["ZDTXPWD"]  # 改为你的密码
MAIL1 = os.environ["MAIL1"]
M1PW = os.environ["M1PW"]
MAIL2 = os.environ["MAIL2"]
flag = False
a = (random.randint(0, 2100)) / 1000000
b = (random.randint(0, 2100)) / 1000000
lat = 34.7155
lng = 113.6450
lat = round(lat + a, 6)
lng = round(lng + b, 6)
#run_time = time.strftime('%Y{y}%m{m}%d{d} %H:%M',time.localtime()).format(y='年',m='月',d='日',h='时',f='分',s='秒')

# 指点天下登录模块
def login():
    url = 'http://app.zhidiantianxia.cn/api/Login/pwd'
    encoded_pwd = md5('axy_{}'.format(pwd).encode()).hexdigest()
    global flag
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '177',
        'Host': 'app.zhidiantianxia.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.10.0'
    }
    data = {
        'phone': phone,
        'password': encoded_pwd,
        'mobileSystem': '11',
        'appVersion': '1.6.5',
        'mobileVersion': 'M2011K2C',
        'deviceToken': '160a3797c8a6df4ff07',  # 随意更改几位16进制字符(0-F)
        'pushToken': '18697781978',  # 可随意更改几位字符
        'romInfo': 'mi'
    }
    response = session.post(url=url, headers=header, data=data)
    if response.json()['status'] == 1:
        print('登录成功！')
        flag = True
    else:
        print('登录失败！', response.json()['msg'])
    return response.json()['data']


# 获取signinid
def get_signInId(token):
    url = 'http://zua.zhidiantianxia.cn/applets/signin/my'
    header = {
        'axy-phone': phone,
        'axy-token': token,
        'user-agent': 'M2011K2C(Android/11) (com.axy.zhidian/1.6.3) Weex/0.18.0 1080x1920',
        'Host': 'zua.zhidiantianxia.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    data = {
        'page': '0',
        'size': '10'
    }
    result = session.get(url=url, headers=header, data=data)
    try:
        signInId = session.get(url=url, headers=header, data=data).json()['data']['content'][0]['id']
        return signInId
    except:
        pass


# 日常签到开始
def sign_in_evening(token):
    url = 'http://zua.zhidiantianxia.cn/applets/signin/sign'
    header = {
        'axy-phone': phone,
        'axy-token': token,
        'Content-Type': 'application/json',
        'user-agent': 'MI 6(Android/9) (com.axy.zhidian/1.6.3) Weex/0.18.0 1080x1920',
        'Host': 'zua.zhidiantianxia.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Length': '146'
    }
    data = {
        "locale": "河南省郑州市二七区大学南路7-8号靠近郑州航空工业管理学院南校区", "lat": lat, "lng": lng, "signInId": get_signInId(token)
    }
    data = json.dumps(data)
    response = session.post(url=url, headers=header, data=data)
    
    # 登录你的邮箱
    yag = yagmail.SMTP(user = MAIL1 , password = M1PW, host = 'smtp.qq.com')
    # 发送邮件
    if response.json()['status'] == 1:
        print("签到成功！")
        yag.send(to = [MAIL2], subject = '指点天下日常签到结果', contents = ['亲爱的臭臭酱，今天的签到已经完成啦！！！'])
        
    else:
        print("签到失败！")
        yag.send(to = [MAIL12], subject = '指点天下日常签到结果', contents = ['亲爱的臭臭酱，本次签到失败啦！原因是：{}。详情请打开指点天下APP查看哦！'.format(response.json()['msg'])])
        

token = login()
sleep(5)
get_signInId(token)
sleep(4)
if flag:
    sign_in_evening(token)
