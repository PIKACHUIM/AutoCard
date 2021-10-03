#!/usr/bin/python3
# coding=utf-8

# --------------------------------------------
#
#       四川大学SCU健康每日报自动打卡平台
#                 邮件通知服务
#
#    AutoCard for SCU 2019-nCov Application
#                 Mail Service
#
#                 Version 2.3
#
#    Code By Pikachu & Updated on MAR30/2021
#    ©2020-2021 Pikachu. All Rights Reserved
# --------------------------------------------
global times
import re
import sys
import time
import json
import signal
import logging
import smtplib
import pymysql
import requests
import datetime
from email.mime.text import MIMEText

class TimeoutError(Exception):
    def __init__(self, msg):
        super(TimeoutError, self).__init__()
        self.msg = msg
 
 
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
 
 
def timeout_callback(e):
    debugLog('网络错误', '网络错误：连接超时，3秒后将继续')
    time.sleep(3)


logging.captureWarnings(True)
# ------------------------------------------------------系统全局设置------------------------------------------------------
statucode = ['打卡成功', '系统故障', '登录失败', '已经填过', '获取失败', '其他错误']
detailnum = ['恭喜！今日打卡已经成功',
             '请手动打卡等待系统修复',
             '请检查用户密码是否正确',
             '今日已经填过无需再打卡',
             '无法获取昨日打卡信息！',
             '未知错误, 自行检查打卡']
loginUrls = "https://ua.scu.edu.cn/login?service=https%3A%2F%2Fwfw.scu.edu.cn%2Fa_scu%2Fapi%2Fsso%2Fcas-index" \
            "%3Fredirect%3Dhttps%253A%252F%252Fwfw.scu.edu.cn%252Fncov%252Fwap%252Fdefault%252Findex"
postsUrls = "https://wfw.scu.edu.cn/ncov/wap/default/save"
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


# -----------------------------------------------------调试信息输出-------------------------------------------------------
def debugLog(in_head, in_info, in_leve=0):
    global times
    infos = ['信息', '成功', '失败', '警告', '错误', '恐慌']
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "[" + in_head + "][" + infos[in_leve] + "]：", in_info)
    with open("./run/" + times + ".log", "a") as files:
        files.write(str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "[" + in_head + "][" + infos[in_leve] + "]：" + str(
                in_info)) + "\n")
    files.close()

    
@time_out(9, timeout_callback)
def sendmail(in_head, title_text, infos_text, detai_text, tails_text, cards_user, mysql_dat2, mail_sets):
    try:
        mailPost(title_text + infos_text + detai_text + tails_text, mail_sets, "【SCU自动打卡系统】" + in_head,
        mysql_dat2[0][2], mysql_dat2[1][2], mysql_dat2[2][2], mysql_dat2[3][2], mysql_dat2[4][2])
        return True
    except BaseException or IOError:
        debugLog('邮件发送', '邮件发送异常！！！！', 2)
        return False

# -----------------------------------------------------自动打卡程序-------------------------------------------------------
def autoMail(in_head, in_text, in_bgat=0, in_ends=9999999999999):
    debugLog("自动打卡", "-------------------------------")
    debugLog("自动打卡", "开始执行" + datetime.datetime.now().strftime('%Y-%m-%d-%H') + "的邮件任务", 0)
    debugLog("自动打卡", "-------------------------------")
    try:
        with open("config.json", 'r') as load_f:
            mysql_conf = json.load(load_f)
    except pymysql.err.OperationalError or KeyError or FileNotFoundError or Exception:
        debugLog('数据读取', '无法读取JSON！！！', 5)
        return 1
    mysql_sql1 = "SELECT * FROM pc_user WHERE 1".format(1)
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
    loop = 0
    mail = ""
    text = ""
    nums = 0
    maxl = len(mysql_dat1)
    for cards_user in mysql_dat1:
        nums = nums + 1
        if int(cards_user[0]) < in_bgat:
            continue
        if int(cards_user[0]) > in_ends:
            break
        if loop >= 100 or nums==maxl:
            debugLog("开始邮箱", "邮件记录结束: " + text)
            debugLog('当前选中', '当前选中用户学号：' + str(cards_user[0]), 0)
            title_text = "<h2>SCU健康每日报自动打卡系统</h2><br />"
            # infos_text = "你好，账号：<b> " + str(cards_user[0]) + "</b>，下列消息值得你关注："
            infos_text = "你好，下列消息值得你关注："
            detai_text = "<br />" + in_text + "</b>"
            tails_text = "<br />获取更多信息请访问<a href='http://card.52pika.cn'>皮卡丘自动打卡平台</a>"
            sendmail(in_head, title_text, infos_text, detai_text, tails_text, cards_user, mysql_dat2, mail)
            mail = ""
            loop = 0
        else:
            pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
            text = cards_user[2].replace('\n','')
            text = text.replace('\r','')
            if re.match(pattern,text) is not None:
                if loop != 0:
                    mail = mail + ',' 
                else:
                    debugLog("开始邮箱", "邮件记录开始: " + text)
                mail = mail + text
            loop = loop + 1
    mysql_conn.close()
    debugLog("自动打卡", "-------------------------------")
    debugLog("自动打卡", "成功完成" + datetime.datetime.now().strftime('%Y-%m-%d-%H') + "的邮件任务", 0)
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
        elif pcrt == 'None':
            sendmsg = smtplib.SMTP(host, port)
            
            sendmsg.ehlo()
        else:
            return 2
        sendmsg.login(yxzh, yxmm)
        sendmsg.sendmail(yxzh, mail, message.as_string())
        debugLog('邮件发送', '成功发送邮件：' + mail, 1)
        sendmsg.quit()
        return 0
    except BaseException as e:
        debugLog('邮件发送', '无法发送邮件：' + mail, 2)
        print(e)
        return 1


# -----------------------------------------------------主要调用入口-------------------------------------------------------
if __name__ == '__main__':
    global times
    times = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    if len(sys.argv) > 5:
        autoMail(sys.argv[1], sys.argv[2], int(sys.argv[4]), int(sys.argv[5]))
    elif len(sys.argv) > 4:
        autoMail(sys.argv[1], sys.argv[2], int(sys.argv[4]), 9999999999999)
    elif len(sys.argv) > 3:
        autoMail(sys.argv[1], sys.argv[2], 0,                9999999999999)
    elif len(sys.argv) > 2:
        autoMail(sys.argv[1], sys.argv[2], 0,                9999999999999)
    else:
        debugLog("执行失败", "Usage: notice <Text> <Flag> <Begin>")

# ----------------------------------------------------------------------------------------------------------------------
