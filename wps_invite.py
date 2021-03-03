# coding=utf-8
import requests
import pytz
import datetime
from io import StringIO
import time
import os
import yagmail

# 初始化信息
MAIL1 = os.getenv('MAIL1')
M1PW = os.getenv('M1PW')
MAIL2 =  os.getenv('MAIL2')
WPS_ID = os.getenv('WPS_ID')
WPS_SID = os.getenv('WPS_SID')
#a = 0

#SCKEY = 'SCT13711Ta6e2FTvd5UHDgH6QuDWl7iHP'  # '*********复制SERVER酱的SCKEY进来*************(保留引号)'
data = {
    "wps_invite": [
        {
            "name": "臭臭酱",
            "invite_userid": 248098774,  # "*********复制手机WPS个人信息中的用户ID进来，类似括号内容(123456789)*************(不保留双引号)",
            "sid": WPS_SID  # network获取wps_sid
        }
    ]
}
# 初始化日志
sio = StringIO('WPS签到日志\n\n')
sio.seek(0, 2)  # 将读写位置移动到结尾
s = requests.session()
tz = pytz.timezone('Asia/Shanghai')
nowtime = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
sio.write("-" + nowtime + "-\n\n")

# APP
def pushMail(desp, nowtime):
    #ssckey = SCKEY
    #send_url = 'https://sctapi.ftqq.com/' + ssckey + '.send'
    yag = yagmail.SMTP(user = MAIL1, password = M1PW, host = 'smtp.qq.com')
    if '失败' in desp:
        yag.send(to = [MAIL2], subject = 'WPS小程序邀请结果：', contents = ['亲爱的臭臭酱，本次邀请失败啦！原因是：\n{}。详情请打开WPS微信小程序查看哦！'.format(desp)])
    else:
        yag.send(to = [MAIL2], subject = 'WPS小程序邀请结果：', contents = ['亲爱的臭臭酱，本次邀请成功啦！本次共邀请了10人。详情请打开WPS微信小程序查看哦！']) #本次共邀请了{}人。详情请打开WPS微信小程序查看哦！'.format(PCOUNT)
        


# 主函数
def main():
    wps_inv = data['wps_invite']
    # 这13个账号被邀请
    invite_sid = [
        "V02StVuaNcoKrZ3BuvJQ1FcFS_xnG2k00af250d4002664c02f",
        "V02SWIvKWYijG6Rggo4m0xvDKj1m7ew00a8e26d3002508b828",
        "V02Sr3nJ9IicoHWfeyQLiXgvrRpje6E00a240b890023270f97",
        "V02SBsNOf4sJZNFo4jOHdgHg7-2Tn1s00a338776000b669579",
        "V02ScVbtm2pQD49ArcgGLv360iqQFLs014c8062e000b6c37b6",
        "V02S2oI49T-Jp0_zJKZ5U38dIUSIl8Q00aa679530026780e96",
        "V02ShotJqqiWyubCX0VWTlcbgcHqtSQ00a45564e002678124c",
        "V02SFiqdXRGnH5oAV2FmDDulZyGDL3M00a61660c0026781be1",
        "V02S7tldy5ltYcikCzJ8PJQDSy_ElEs00a327c3c0026782526",
        "V02SPoOluAnWda0dTBYTXpdetS97tyI00a16135e002684bb5c",
        "V02Sb8gxW2inr6IDYrdHK_ywJnayd6s00ab7472b0026849b17",
        "V02SwV15KQ_8n6brU98_2kLnnFUDUOw00adf3fda0026934a7f",
        "V02SC1mOHS0RiUBxeoA8NTliH2h2NGc00a803c35002693584d"

    ]
    for item in wps_inv:
        sio.write("为{}邀请---↓\n\n".format(item['name']))
        if type(item['invite_userid']) == int:
            wps_invite(invite_sid, item['invite_userid'])
            time.sleep(10)
        else:
            sio.write("邀请失败：用户ID错误，请重新复制手机WPS个人信息中的用户ID并修改'invite_userid'项,注意不保留双引号\n\n")
    desp = sio.getvalue()
    pushMail(desp, nowtime)
    print(desp)
    return desp

# wps接受邀请
def wps_invite(sid: list, invite_userid: int) -> None:
    invite_url = 'http://zt.wps.cn/2018/clock_in/api/invite'
    for index, i in enumerate(sid):
        headers = {
            'sid': i
        }
        time.sleep(10)
        r = s.post(invite_url, headers=headers, data={
            'invite_userid': invite_userid})
        #a = a + 1

def main_handler(event, context):
    return main()

if __name__ == '__main__':
    main()
