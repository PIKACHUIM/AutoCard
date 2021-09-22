#!/usr/bin/python3
# coding=utf-8

# --------------------------------------------
#
#       四川大学SCU健康每日报自动打卡平台
#                 打卡核心程序
#
#    AutoCard for SCU 2019-nCov Application
#                 Core Service
#
#                 Version 2.4
#
#    Code By Pikachu & Updated on SEP20/2021
#    ©2020-2021 Pikachu. All Rights Reserved
# --------------------------------------------

import re
import sys
import time
import json
global times
import signal
import logging
import smtplib
import pymysql
import muggle_ocr
import requests
import datetime
sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

from email.mime.text import MIMEText

# 超时类主体 -----------------------------------------------------------------------------------------------------
class TimeoutError(Exception):
    def __init__(self, msg):
        super(TimeoutError, self).__init__()
        self.msg = msg
 
# 认证超时函数代理 ------------------------------------------------------------------------------------------------
def time_out(interval, callback):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError("Run Func Timeout")
 
        def wrapper(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(interval)       # interval秒后向进程发送SIGALRM信号
                result = func(*args, **kwargs)
                signal.alarm(0)              # 函数在规定时间执行完后关闭alarm闹钟
                return result
            except TimeoutError or json.decoder.JSONDecodeError as e:
                callback(e)
        return wrapper
    return decorator
 
# 超时回调函数主体 ------------------------------------------------------------------------------------------------
def timeout_callback(e):
    debugLog('网络错误', '网络错误：连接超时，3秒后将继续')
    time.sleep(3)


logging.captureWarnings(True)
# ------------------------------------------------------系统全局设置------------------------------------------------
statucode = ['打卡成功', '系统故障', 
             '登录失败', '已经填过',
             '获取失败', '其他错误',
             '验证失败', '未知错误']
detailnum = ['恭喜！今日打卡已经成功',
             '请手动打卡等待系统修复',
             '请检查用户密码是否正确',
             '今日已经填过无需再打卡',
             '无法获取昨日打卡信息！',
             '未知错误, 自行检查打卡',
             '验证码获取或者识别失败',
             '遇到未知错误，打卡失败']
loginUrls = "https://ua.scu.edu.cn/login?service=https%3A%2F%2Fwfw.scu.edu.cn%2Fa_scu%2Fapi%2Fsso%2Fcas-index" \
            "%3Fredirect%3Dhttps%253A%252F%252Fwfw.scu.edu.cn%252Fncov%252Fwap%252Fdefault%252Findex"
postsUrls = "https://wfw.scu.edu.cn/ncov/wap/default/save"
codesUrls = 'https://ua.scu.edu.cn/captcha?captchaId=' 
PostHeads = {
    'Host': 'wfw.scu.edu.cn',
    'Origin': 'https://wfw.scu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25'
                  ' Safari/537.36 Core/1.70.3754.400 QQBrowser/10.5.4034.400',
    'Accept-Encoding': "gzip, deflate, br",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Content-Type': 'application/x-www-form-urlencoded',
    'Pragma': 'no-cache',
    'Referer': 'https://ua.scu.edu.cn/login?service=https%3A%2F%2Fwfw.scu.edu.cn%2Fa_scu%2Fapi%2Fsso%'
               '2Fcas-index%3Fredirect%3Dhttps%253A%252F%252Fwfw.scu.edu.cn%252Fncov%252Fwap%252Fdefault%252Findex',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
}


# -----------------------------------------------------调试信息输出-----------------------------------------------------
def debugLog(in_head, in_info, in_leve=0):
    global times
    infos = ['信息', '成功', '失败', '警告', '错误', '恐慌', '不幸']
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "[" + in_head + "][" + infos[in_leve] + "]：", in_info)
    with open("./run/" + times + ".log", "a") as files:
        files.write(str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "[" + in_head + "][" + infos[in_leve] + "]：" + str(
                in_info)) + "\n")
    files.close()

# 执行函数主体 ----------------------------------------------------------------------------------------------------------
@time_out(5, timeout_callback)
def timeouts(cards_user):
    cards_sesi = requests.Session()
    cards_data = usrLogin(cards_user[0], cards_user[1], cards_sesi)
    cards_sesi.close()
    return cards_data

# 主超时函数认证 --------------------------------------------------------------------------------------------------------
@time_out(9, timeout_callback)
def sendmail(title_text, infos_text, detai_text, tails_text, cards_user, mysql_dat2):
    try:
        mailPost(title_text + infos_text + detai_text + tails_text, cards_user[2],
        "【SCU自动打卡系统】" + time.strftime("%Y-%m-%d", time.localtime()) + "的打卡",
        mysql_dat2[0][2], mysql_dat2[1][2], mysql_dat2[2][2], mysql_dat2[3][2], mysql_dat2[4][2])
        return True
    except BaseException or IOError:
        debugLog('邮件发送', '邮件发送异常！！！！', 2)
        return False

# -----------------------------------------------------提交打卡程序-------------------------------------------------------
def postCard(in_sesi, in_data):
    try:
        cards_temp = eval(in_data[0])
        cards_temp['date'] = time.strftime("%Y%m%d", time.localtime(time.time()))
        cards_info = in_sesi.post(url=postsUrls, headers=PostHeads, data=cards_temp).json()
        if '今天已经填报了' in cards_info['m']:
            return 3
        elif '操作成功' in cards_info['m']:
            return 0
        else:
            return 5
    except requests.exceptions.ConnectionError or BaseException or ValueError:
        return 1


# ----------------------------------------------------登录认证函数---------------------------------------------------------
def usrLogin(in_user, in_pass, in_sesi):
    try_times = 5
    try:
        login_sesi = in_sesi
        login_info = login_sesi.get(url=loginUrls,
                                    headers=PostHeads,
                                    verify=False)
    except requests.exceptions.ConnectionError or BaseException:
        return 1
    # 获取会话验证信息 --------------------------------------------------
    login_even = login_info.text.find('execution')
    login_seid = login_info.text.find('_eventId')
    if login_even>0 and login_seid>0:
        try:
            login_exec = login_info.text[login_even + 18:login_seid - 16]
        except ValueError or BaseException:
            return 4
    # 获取验证码code值 --------------------------------------------------
    login_code = login_info.text.find('config.captcha')
    if login_code >0 :
        try:
            login_very = login_info.text[login_code + 47:login_code + 57]
        except ValueError or BaseException:
            login_very = "ERROR"
            debugLog('验证获取', 'RequestGet验证码获取失败!!!!!!!', 1)
            return 6
    else:
        debugLog('验证获取', 'RequestGet验证码获取失败!!!!!!!', 1)
        return 6
    debugLog('验证获取', '已获得本次验证码ID:  '+login_very, 1)
    # 验证码识别过程 ----------------------------------------------------
    
    try:
        login_info = login_sesi.get(url=codesUrls+str(login_very),
                                     headers=PostHeads,
                                     verify=False)
        with open('captcha.jpg', 'wb') as file:
            file.write(login_info.content)
        with open(r"captcha.jpg", "rb") as file:
            captcha_bytes = file.read()
            text = sdk.predict(image_bytes=captcha_bytes)
            if len(text)<6:
                debugLog('验证获取', 'Muggle-OCR验证码获取失败!!!!!!!', 1)
                return 6
            debugLog('验证获取', 'Muggle-OCR识别的验证码:  '+ text.lower(), 1)
    except requests.exceptions.ConnectionError as e:
        debugLog('验证获取', e, 2)
        return 6
    except BaseException as e:
        debugLog('验证获取', e, 2)
        return 6
    # 提交登录验证请求 --------------------------------------------------
    login_data = {
        'username': str(in_user),
        'password': str(in_pass),
        'submit': '登录',
        'captcha': text, 
        'type': 'username_password',
        '_eventId': 'submit',
        'execution': login_exec
    }
    try:
        login_info = login_sesi.post(url=loginUrls,
                                     data=login_data,
                                     headers=PostHeads,
                                     verify=False)
    except requests.exceptions.ConnectionError or BaseException:
        return 1
    if login_info.text.find('川大疫情防控每日报系统') < 0:
        if login_info.text.find('移动微服务') >= 0:
            return 6
        else:
            return 1
    file_name = 'jpg/'+time.strftime("%Y%m%d%H%M%S", time.localtime())+"-"+text.lower()+".jpg"
    with open(r"captcha.jpg", "rb") as file:
        with open(file_name, 'wb') as imgs:
                imgs.write(file.read())
    try:
        login_last = re.findall(r'.*?oldInfo: (.*),.*?', login_info.text)
    except ValueError or BaseException:
        return 4
    if login_last == '':
        return 4
    debugLog('开始打卡', '用户登录成功, 开始执行打卡进程!')
    return postCard(in_sesi, login_last)


# -----------------------------------------------------自动打卡程序-------------------------------------------------------
def autoCard(in_flag, in_time):
    debugLog("自动打卡", "-------------------------------")
    debugLog("自动打卡", "开始执行" + datetime.datetime.now().strftime('%Y-%m-%d-%H') + "的打卡任务", 0)
    debugLog("自动打卡", "-------------------------------")
    cards_nums = 0
    try:
        with open("config.json", 'r') as load_f:
            mysql_conf = json.load(load_f)
    except pymysql.err.OperationalError or KeyError or FileNotFoundError or Exception:
        debugLog('数据读取', '无法读取JSON！！！', 5)
        return 1
    mysql_sql1 = "SELECT * FROM pc_user WHERE flag = 1".format(1)
    mysql_sql2 = "SELECT * FROM pc_info".format(1)
    try:
        mysql_conn = pymysql.connect(host=mysql_conf['db_host'],
                                     port=mysql_conf['db_port'],
                                     user=mysql_conf['db_user'],
                                     password=mysql_conf['db_pass'],
                                     db=mysql_conf['db_name'])
    except BaseException or pymysql.err.ProgrammingError as cards_errs:
        debugLog('数据读取', '无法连接数据:' + str(cards_errs), 5)
        return 1
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(mysql_sql1)
            mysql_dat1 = cursor.fetchall()
        mysql_conn.commit()
        with mysql_conn.cursor() as cursor:
            cursor.execute(mysql_sql2)
            mysql_dat2 = cursor.fetchall()
        mysql_conn.commit()
    except pymysql.err.ProgrammingError or BaseException as cards_errs:
        mysql_conn.rollback()
        debugLog('数据读取', '无法获取用户:' + str(cards_errs), 5)
        return 1
    for cards_user in mysql_dat1:
        if in_time != cards_user[7] and in_time != -1:
            continue
        time.sleep(1)
        cards_nums = cards_nums + 1
        debugLog("自动打卡", "-------------------------------")
        debugLog('当前选中', '当前选中用户学号：' + str(cards_user[0]), 0)
        cards_flag = 10
        while cards_flag > 0:
            cards_data = timeouts(cards_user)
            if cards_data is not None:
                if cards_data!=0:
                    # 未知错误 --------------------------------------------------------------
                    if cards_data==7:
                        debugLog('打卡结果', statucode[cards_data]+','+detailnum[cards_data])
                        cards_flag = 0
                    # 未知错误 --------------------------------------------------------------
                    elif cards_data==6:
                        debugLog('打卡结果', '用户名/密码/验证码不正确, 重试!')
                    # 未知错误 --------------------------------------------------------------
                    elif cards_data==5:
                        debugLog('打卡结果', statucode[cards_data]+','+detailnum[cards_data])
                    # 未知错误 --------------------------------------------------------------
                    elif cards_data==4:
                        debugLog('打卡结果', statucode[cards_data]+','+detailnum[cards_data])
                    # 未知错误 --------------------------------------------------------------
                    elif cards_data==3:
                        debugLog('打卡结果', statucode[cards_data]+','+detailnum[cards_data])
                        cards_flag = 0
                        break
                    # 未知错误 --------------------------------------------------------------
                    elif cards_data==2:
                        debugLog('打卡结果', statucode[cards_data]+','+detailnum[cards_data])
                        cards_flag = 0
                    # 未知错误 --------------------------------------------------------------
                    elif cards_data==1:
                        debugLog('打卡结果', statucode[cards_data]+','+detailnum[cards_data])
                else:
                    debugLog('打卡结果', statucode[cards_data] + ',' + detailnum[cards_data], cards_data)
                    cards_flag = 0
                    break
            if cards_flag <= 1:
                debugLog('打卡结果', '此用户全部打卡尝试失败,跳过打卡')
                break
            else:
                debugLog('打卡结果', '第'+ str(11-cards_flag)+'次打卡尝试失败，即将重试打卡')
                cards_flag = cards_flag -1
        title_text = "<h2>SCU健康每日报自动打卡系统</h2><br />"
        infos_text = "你好，你的账号：<b> " + str(cards_user[0]) + "<br /></b>今日的打卡情况：" + statucode[cards_data]
        detai_text = "<br />系统详细信息：<b>" + detailnum[cards_data] + "</b>"
        tails_text = "<br />获取更多信息请访问<a href='http://card.52pika.cn'>皮卡丘自动打卡平台</a>"
        if cards_data == 0:
            mysql_sql3 = ("UPDATE pc_user SET succ=" + str(int(cards_user[3]) + 1) + " WHERE user=" + str(
                cards_user[0])).format(1)
        else:
            mysql_sql3 = ("UPDATE pc_user SET fail=" + str(int(cards_user[4]) + 1) + " WHERE user=" + str(
                cards_user[0])).format(1)
        try:
            mysql_sql4 = ("INSERT INTO pc_logs (dkid,time,user,flag,info) VALUES ("
                          + "'" + str(int(datetime.datetime.now().strftime('%y%m%d%H%M')) * 10000 + cards_nums) + "',"
                          + "'" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "',"
                          + "'" + str(cards_user[0]) + "',"
                          + "'" + statucode[cards_data] + "',"
                          + "'" + detailnum[cards_data] + "'"
                          + ")").format(1)
            with mysql_conn.cursor() as cursor:
                cursor.execute(mysql_sql3)
                cursor.execute(mysql_sql4)
            mysql_conn.commit()
        except pymysql.err.IntegrityError or pymysql.err.IntegrityError or ValueError or BaseException:
            debugLog('数据操作', '日志写入异常！！！！！！！！！！', 3)
            mysql_conn.rollback()
        if in_flag and (int(cards_user[6]) == 1 or int(cards_data) > 3 or (0 < int(cards_data) < 3)):
            #sendmail(title_text, infos_text, detai_text, tails_text, cards_user, mysql_dat2)
            pass
    mysql_conn.close()
    debugLog("自动打卡", "-------------------------------")
    debugLog("自动打卡", "成功完成" + datetime.datetime.now().strftime('%Y-%m-%d-%H') + "的打卡任务", 0)
    debugLog("自动打卡", "-------------------------------")


# -----------------------------------------------------邮件发送程序-------------------------------------------------------
def mailPost(text, mail, head, yxzh, yxmm, host, port=465, pcrt='SSL'):
    subject = head
    content = text
    message = MIMEText(content, 'html', 'utf-8')
    message['Subject'] = subject
    message['From'] = yxzh
    message['To'] = mail
    try:
        if pcrt == 'SSL':
            sendmsg = smtplib.SMTP_SSL(host, port)
        elif pcrt == 'TLS':
            sendmsg = smtplib.SMTP(host, port)
            sendmsg.ehlo()
            sendmsg.starttls()
        else:
            return 2
        sendmsg.login(yxzh, yxmm)
        sendmsg.sendmail(yxzh, mail, message.as_string())
        debugLog('邮件发送', '成功发送邮件：' + mail, 1)
        sendmsg.quit()
        return 0
    except BaseException or IOError or ValueError as e:
        debugLog('邮件发送', '无法发送邮件：' + mail, 2)
        print(e)
        return 1


# -----------------------------------------------------主要调用入口-------------------------------------------------------
if __name__ == '__main__':
    global times
    times = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    main_mail = True
    main_time = 4
    if len(sys.argv) > 1:
        for ptrs in sys.argv:
            if ptrs == 'nomail':
                main_mail = False
            elif ptrs == "time00":
                main_time = 1
            elif ptrs == "time07":
                main_time = 2
            elif ptrs == "time09":
                main_time = 0
            elif ptrs == "time11":
                main_time = 3
            elif ptrs == "timeXX":
                main_time = -1
            else:
                pass
    if main_time == 4:
        cards_time = int(datetime.datetime.now().strftime('%H'))
        if cards_time < 7:
            main_time = 1
        elif 7 <= cards_time < 9:
            main_time = 2
        elif 9 <= cards_time < 11:
            main_time = 0
        else:
            main_time = 3
    autoCard(main_mail, main_time)

# ----------------------------------------------------------------------------------------------------------------------
