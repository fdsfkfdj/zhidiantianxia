#!/usr/bin/python3
# -*- coding: utf-8 -*
#version:python 3.8.6

import requests
import json
from hashlib import md5
from time import sleep
import time
import yagmail
import os

session = requests.Session()
PHONE = os.environ["PHONE"]
ZDTXPWD =  os.environ["ZDTXPWD"]
MAIL1 = os.environ["MAIL1"]
M1PW = os.environ["M1PW"]
MAIL2 = os.environ["MAIL2"]
flag = False

#指点天下登录模块
def login():
    print(ZDTXPWD)
    url = 'http://app.zhidiantianxia.cn/api/Login/pwd'
    encoded_pwd = md5('axy_{}'.format(ZDTXPWD).encode()).hexdigest()
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
        'phone':PHONE,
        'password':encoded_pwd,
        'mobileSystem':'11',
        'appVersion':'1.6.5',
        'mobileVersion':'M2011K2C',
        'deviceToken':'160a3797c8a6df4ff07',  #随意更改几位16进制字符(0-F)
        'pushToken':'18697781978',  #可随意更改几位字符
        'romInfo':'mi'
    }
    response = session.post(url=url,headers=header,data=data)
    if response.json()['status'] == 1:
        print('登录成功！')
        flag = True
    else:
        print('登录失败！',response.json()['msg'],PHONE,PWD,MAIL1,M1PW,MAIL2)
    return response.json()['data']

#健康签到模块
def sign_in(token):
    url = 'http://zua.zhidiantianxia.cn/api/study/health/apply'
    header = {
        'axy-phone': PHONE,
        'axy-token': token,
        'Content-Type': 'application/json',
        'user-agent': 'M2011K2C(Android/11) (com.axy.zhidian/1.6.3) Weex/0.18.0 1080x1920',
        'Host': 'zua.zhidiantianxia.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Length': '679'
    }
    data = {
        "health":0,
        "student":1,
        "templateId":"1","content":"{\"location\":{\"address\":\"河南省郑州市二七区大学南路7-6号靠近万达广场\",\"code\":\"1\",\"lng\":113.644864,\"lat\":34.717667},\"nowLocation\":\"河南省-郑州市-二七区\",\"temperature\":\"36.6\",\"health\":\"是\",\"observation\":\"否\",\"confirmed\":\"否\",\"goToHuiBei\":\"否\",\"contactIllPerson\":\"否\",\"isFamilyStatus\":\"否\",\"help\":\"\"}"
        }
    data = json.dumps(data)
    response = session.post(url=url,headers=header,data=data)
    

    if response.json()['status'] == 1:
        print("健康打卡成功！")
        yag = yagmail.SMTP(user = MAIL1, password = M1PW, host = 'smtp.qq.com')
        yag.send(to = [MAIL2], subject = '指点天下健康签到结果', contents = ['亲爱的臭臭酱，今天的健康签到已经完成啦！今天也会是健健康康的一天哦！！！'])
    else:
        print("健康打卡失败！",response.json()['msg'])
        result = response.json()['msg']
        yag = yagmail.SMTP(user = MAIL1, password = M1PW, host = 'smtp.qq.com')
        yag.send(to = [MAIL2], subject = '指点天下健康签到结果', contents = ['亲爱的臭臭酱，今天的健康签到失败了哦。原因是：{}。具体原因请打开指点天下APP查看。'.format(result)])



token = login()
sleep(5)
if flag:
    sign_in(token)
    
