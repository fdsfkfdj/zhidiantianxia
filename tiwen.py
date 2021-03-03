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
PHONE = os.environ ['PHONE']
PWD = os.environ ['PWD']
NAIL1 = os.environ ['MAIL1']
M1PW = os.environ ['M1PW']
MAIL2 = os.environ ['MAIL2']
flag = False

#指点天下登录模块
def login():
    url = 'http://app.zhidiantianxia.cn/api/Login/pwd'
    encoded_pwd = md5('axy_{}'.format(PWD).encode()).hexdigest()
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
        print('登录失败！',response.json()['msg'])
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
        "student":"1",
        "content": "{\"location\":{\"address\":\"福建省厦门市海沧区G76厦蓉高速1394号靠近厦门欣昱机电有限公司\",\"code\":\"1\",\"lng\":117.993856,\"lat\":24.469346},\"name\":\"方祖全\",\"phone\":\"18697781978\",\"credentialType\":\"身份证\",\"credentialCode\":\"411503199810144239\",\"college\":\"航空工程学院\",\"major\":\"机械设计制造及其自动化S\",\"className\":\"19069601班\",\"code\":\"1906960136\",\"nowLocation\":\"福建省-厦门市-海沧区\",\"temperature\":\"36.6\",\"observation\":\"否\",\"confirmed\":\"否\",\"goToHuiBei\":\"否\",\"contactIllPerson\":\"否\",\"isFamilyStatus\":\"否\",\"health\":0}"
        }
    data = json.dumps(data)
    response = session.post(url=url,headers=header,data=data)
    
    # 登录你的邮箱
    yag = yagmail.SMTP(user = MAIL1, password = M1PW, host = 'smtp.qq.com')

    if response.json()['status'] == 1:
        print("健康打卡成功！")
        yag.send(to = [MAIL2], subject = '指点天下健康签到结果', contents = ['亲爱的臭臭酱，今天的健康签到已经完成啦！今天也会是健健康康的一天哦！！！'])
    else:
        print("健康打卡失败！",response.json()['msg'])
        result = response.json()['msg']
        yag.send(to = [MAIL2], subject = '指点天下健康签到结果', contents = ['亲爱的臭臭酱，今天的健康签到失败了哦。原因是：{}。具体原因请打开指点天下APP查看。'.format(result)])



token = login()
sleep(5)
if flag:
    sign_in(token)
