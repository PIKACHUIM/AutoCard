#!/usr/bin/python3
# coding=utf-8
import re
import sys
import time
import json
import logging
import smtplib
import pymysql
import requests
import datetime
from email.mime.text import MIMEText

logging.captureWarnings(True)
# ------------------------------------------------------系统全局设置------------------------------------------------------
statucode = ['打卡成功', '系统故障', '登录失败', '已经填过', '获取失败', '其他错误']
detailnum = ['恭喜！！今日打卡已经成功',
             '请手动打卡并等待系统修复',
             '请检查用户名密码是否正确',
             '今日已经填过，无需再打卡',
             '无法获取昨日打卡信息！！',
             '未知错误，请自行检查打卡']
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
    infos = ['信息', '成功', '失败', '警告', '错误', '恐慌']
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "[" + in_head + "][" + infos[in_leve] + "]：", in_info)


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


# ----------------------------------------------------登录认证函数--------------------------------------------------------
def usrLogin(in_user, in_pass, in_sesi):
    try:
        login_sesi = in_sesi
        login_info = login_sesi.get(url=loginUrls, headers=PostHeads, verify=False)
    except requests.exceptions.ConnectionError or BaseException:
        return 1
    if login_info.text.find('execution') > 0 and login_info.text.find('_eventId') > 0:
        try:
            login_exec = login_info.text[login_info.text.find('execution') + 18:login_info.text.find('_eventId') - 16]
        except ValueError or BaseException:
            return 4
    else:
        return 1
    login_data = {
        'username': str(in_user),
        'password': str(in_pass),
        'submit': '登录',
        'type': 'username_password',
        '_eventId': 'submit',
        'execution': login_exec
    }
    try:
        login_info = login_sesi.post(url=loginUrls, data=login_data, headers=PostHeads, verify=False)
    except requests.exceptions.ConnectionError or BaseException:
        return 1
    if login_info.text.find('川大疫情防控每日报系统') < 0:
        if login_info.text.find('移动微服务') >= 0:
            return 2
        else:
            return 1
    try:
        login_last = re.findall(r'.*?oldInfo: (.*),.*?', login_info.text)
    except ValueError or BaseException:
        return 4
    if login_last == '':
        return 4
    return postCard(in_sesi, login_last)


# -----------------------------------------------------自动打卡程序-------------------------------------------------------
def autoCard(in_flag):
    debugLog("自动打卡", "开始执行" + datetime.datetime.now().strftime('%Y-%m-%d-%H') + "的打卡任务", 0)
    cards_time = int(datetime.datetime.now().strftime('%H'))
    cards_nums = 0
    if cards_time < 7:
        cards_hour = 1
    elif 7 <= cards_time < 9:
        cards_hour = 2
    elif 9 <= cards_time < 11:
        cards_hour = 0
    else:
        cards_hour = 3
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
        if cards_hour != cards_user[7]:
            continue
        time.sleep(10)
        cards_nums = cards_nums + 1
        debugLog('当前选中', '当前选中用户学号：' + str(cards_user[0]), 0)
        cards_sesi = requests.Session()
        cards_data = usrLogin(cards_user[0], cards_user[1], cards_sesi)
        title_text = "<h2>SCU健康每日报自动打卡系统</h2><br />"
        infos_text = "你好，你的账号：<b> " + str(cards_user[0]) + "<br /></b>今日的打卡情况：" + statucode[cards_data]
        detai_text = "<br />系统详细信息：<b>" + detailnum[cards_data] + "</b>"
        tails_text = "<br />获取更多信息请访问<a href='http://card.52pika.cn'>皮卡丘自动打卡平台</a>"
        debugLog('打卡结果', statucode[cards_data] + ', ' + detailnum[cards_data], cards_data)
        if cards_data == 0:
            mysql_sql3 = ("UPDATE pc_user SET succ=" + str(cards_user[4] + 1) + " WHERE user=" + str(
                cards_user[0])).format(1)
        else:
            mysql_sql3 = ("UPDATE pc_user SET fail=" + str(cards_user[5] + 1) + " WHERE user=" + str(
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
            debugLog('数据操作', '日志写入异常！！！！', 3)
            mysql_conn.rollback()
        if in_flag and (int(cards_user[6]) == 1 or int(cards_data) > 3 or (0 < int(cards_data) < 3)):
            try:
                mailPost(title_text + infos_text + detai_text + tails_text, cards_user[2],
                         "【SCU自动打卡系统】" + time.strftime("%Y-%m-%d", time.localtime()) + "的打卡",
                         mysql_dat2[0][2], mysql_dat2[1][2], mysql_dat2[2][2], mysql_dat2[3][2])
            except BaseException or IOError:
                debugLog('邮件发送', '邮件发送异常！！！！', 2)
        cards_sesi.close()
    mysql_conn.close()


# -----------------------------------------------------邮件发送程序-------------------------------------------------------
def mailPost(text, mail, head, yxzh, yxmm, host, port=465):
    subject = head
    content = text
    message = MIMEText(content, 'html', 'utf-8')
    message['Subject'] = subject
    message['From'] = yxzh
    message['To'] = mail
    try:
        sendmsg = smtplib.SMTP(host, port)
        sendmsg.ehlo()
        sendmsg.starttls()
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
    if len(sys.argv) > 1 and sys.argv[1] == 'nomail':
        autoCard(0)
    else:
        autoCard(1)
# ----------------------------------------------------------------------------------------------------------------------
