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


global times
# -----------------------------------------------------调试信息输出-------------------------------------------------------
def debugLog(in_head, in_info, in_leve=0):
    global times
    infos = ['信息', '成功', '失败', '警告', '错误', '恐慌']
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "[" + in_head + "][" + infos[in_leve] + "]：", in_info)
    with open("./run/" + times + ".log", "a") as files:
        files.write(str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "[" + in_head + "][" + infos[in_leve] + "]：" + str(
                in_info))+"\n")
    files.close()


# -----------------------------------------------------自动打卡程序-------------------------------------------------------
def autoMail(in_text, in_time):
    debugLog("自动打卡", "开始执行" + datetime.datetime.now().strftime('%Y-%m-%d-%H') + "的邮件任务", 0)
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
        if in_time != cards_user[7]:
            continue
        time.sleep(10)
        cards_nums = cards_nums + 1
        debugLog('当前选中', '当前选中用户学号：' + str(cards_user[0]), 0)
        cards_sesi = requests.Session()
        title_text = "<h2>SCU健康每日报自动打卡系统</h2><br />"
        infos_text = "你好，你的账号：<b> " + str(cards_user[0]) + "<br /></b>"
        detai_text = "<br />通知信息：<b>" + in_text + "</b>"
        tails_text = "<br />获取更多信息请访问<a href='http://card.52pika.cn'>皮卡丘自动打卡平台</a>"
        try:
            mailPost(title_text + infos_text + detai_text + tails_text, cards_user[2],
                     "【SCU自动打卡系统】" + time.strftime("%Y-%m-%d", time.localtime()) + "的打卡",
                     mysql_dat2[0][2], mysql_dat2[1][2], mysql_dat2[2][2], mysql_dat2[3][2], mysql_dat2[4][2])
        except BaseException or IOError:
            debugLog('邮件发送', '邮件发送异常！！！！', 2)
    mysql_conn.close()


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

if __name__ == '__main__':
    global times
    times = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    if len(sys.argv) > 1:
        autoMail(sys.argv[1])