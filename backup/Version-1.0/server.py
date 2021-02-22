#coding=utf-8
import re
import time
import json
import logging
import smtplib
import requests
from email.mime.text import MIMEText

logging.captureWarnings(True)
#-----------------------------------------------------------------------------------系统全局设置-----------------------------------------------------------------------------------
loginData = {}
loginUrl = "https://wfw.scu.edu.cn/a_scu/api/sso/check"
indexUrl = "https://wfw.scu.edu.cn/ncov/wap/default/index"
postsUrl = "https://wfw.scu.edu.cn/ncov/wap/default/save"
header = {
        'Host': 'wfw.scu.edu.cn',
        'Origin': 'https://wfw.scu.edu.cn',
        'Referer': 'https://wfw.scu.edu.cn/site/polymerization/polymerizationLogin?redirect=https%3A%2F%2Fwfw.scu.edu.cn%2Fncov%2Fwap%2Fdefault%2Findex&from=wap',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3754.400 QQBrowser/10.5.4034.400',
}
#-----------------------------------------------------------------------------------邮件发送模块-----------------------------------------------------------------------------------
def post(text, mail):
    msg_fr = 'pikachuim@qq.com'    # 发送方邮箱
    passwd = 'wdrjlyxvbhftbfge'    # 邮箱授权码
    msg_to = mail                  # 收件人邮箱
    subject = "【SCU自动打卡系统】"+time.strftime("%Y-%m-%d", time.localtime())+"的打卡"
    content = text
    msg = MIMEText(content,'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = msg_fr
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_fr, passwd)
        s.sendmail(msg_fr, msg_to, msg.as_string())
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"【发送成功】：",mail)
    except:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"【发送失败】：",mail)
    finally:
        s.quit()
#-----------------------------------------------------------------------------------自动打卡模块-----------------------------------------------------------------------------------
def zddk(datas, email):
    print('---------------------------------------------------')
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'【正在登录】：',datas['username'])
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'【登录密码】：',datas['password'])
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'【用户邮箱】：',email)
    title = "<h2>SCU健康每日报自动打卡系统</h2><br />"
    infos = "你好，你的账号：<b> "+datas['username']+"<br /></b>今日的打卡情况："
    tails = "<br />获取更多信息请访问<a href='http://card.52pika.cn'>皮卡丘自动打卡平台</a>"
    clien = requests.Session()
    respo = clien.post(url=loginUrl, data=datas, headers=header, verify=False)
    heads = {
        'Host': 'wfw.scu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3754.400 QQBrowser/10.5.4034.400',
        'Accept': 'application/json,text/javascript,*/*;q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip,deflate,br',
        'Content-Type': 'application/x-www-form-urlencoded;',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://wfw.scu.edu.cn',
        'Connection': 'keep-alive',
        'Referer': 'https://wfw.scu.edu.cn/ncov/wap/default/index',
    }
    if respo.text.find("操作成功") != -1:
        #print("【登陆成功】：",datas)
        respo = clien.get(url=indexUrl, headers=header)
        pdata = re.findall(r'.*?oldInfo: (.*),.*?',respo.text)
        strls = pdata[0]
        data = eval(strls)
        data['date'] = time.strftime("%Y%m%d", time.localtime(time.time()))
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'【今天日期】：',data['date'])
        #print(data)
        respo = clien.post(url=postsUrl, headers=heads, data=data).json()
        #print(respo)
        if '今天已经填报了' in respo['m']:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'【已经填过】：', datas['username'])
            post(title+infos+' 已打卡,无法重复打卡'+tails, email)

        elif '操作成功' in respo['m']:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'【填报成功】：', datas['username'])
            post(title+infos+' 恭喜!今日已打卡成功'+tails, email)
        clien.close()
    else:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'【无法登录】：',json.loads(respo.text)['m'])
        post(title+infos+'失败,'+json.loads(respo.text)['m']+tails, email)
#-----------------------------------------------------------------------------------主函数的模块-----------------------------------------------------------------------------------
if __name__ == '__main__':
    print('---------------------------------------------------')
    print('              今天日期：'+time.strftime("%Y-%m-%d", time.localtime()))
    main_file = open("/www/wwwroot/pika_card/passwd.ini")
    for main_line in main_file:
        main_line=main_line.replace('\n','')
        main_temp = []
        try:
            main_temp=main_line.split("|~|")
        except exit():
            pass
        if len(main_temp)==3:
            #print(main_temp)
            tmp={
                "username":main_temp[0],
                "password":main_temp[1],
                "redirect":"https://wfw.scu.edu.cn/ncov/wap/default/index"
            }
            zddk(tmp, main_temp[2])
    main_file.close()
    print('---------------------------------------------------')



