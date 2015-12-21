# coding=utf-8
import re
import time
import requests
import smtplib
import logging
from email.mime.text import MIMEText

# 设置访问信息
UrlIndex  = 'http://lehu.pt'
UrlLogin  = 'http://lehu.pt/takelogin.php'
UrlDaily  = 'http://lehu.pt/api/daily_register.php'
LoginData = {'username': '****', 'password': '****'}

# 设置DEBUG格式
logging.basicConfig(
    level   = logging.INFO,
    format   = '[%(asctime)s] %(message)s',
    datefmt  = '%F %T',
    filename = 'lehu.log',
    filemode = 'a'
)


# 用于签到
def Register():
    # 设置会话对象
    req = requests.Session()

    # 登录
    try:
        # 设置来路信息 尝试登录
        req.headers.update({'Referer': UrlIndex})
        ReqLogin = req.post(UrlLogin, data=LoginData)

        # 解析登录结果
        LoginResult = re.findall(ur'universal_background"><h2>(.*?)<', ReqLogin.content)[0]
        LoginDetail = re.findall(ur'<div class="content">(.*?)<', ReqLogin.content)[0]
        logging.info(LoginResult)
        logging.info(LoginDetail)

        # 登录失败
        if not LoginResult == '登录成功':
            return [False, LoginResult, LoginDetail]

    except Exception, e:
        logging.warn(ReqLogin.content)
        return [False, 'ERROR_1', str(e)]

    # 签到
    try:
        # 获取hash信息 签到
        ReqIndex = req.get(UrlIndex)
        RegHash = re.findall(r"hash: '(.*?)'", ReqIndex.content)
        RegData = {'hash': RegHash}
        ReqDaily = req.post(UrlDaily, data=RegData)

        # 解析签到结果
        RegResult = re.findall(ur'"result":"(.*?)"', ReqDaily.content)[0]
        RegDetail = re.findall(ur'"desc":"(.*?)"', ReqDaily.content)[0]
        RegDetail = RegDetail.decode('raw_unicode_escape')
        logging.info(RegResult)
        logging.info(RegDetail)
        if RegResult == 'ok':
            return [True, '签到成功', RegDetail]
        else:
            return [False, '签到失败', RegDetail]
    except Exception, e:
        logging.warn(ReqDaily.content)
        return [False, 'ERROR_2', str(e)]


# 用于发送邮件
def SendMail(Title, Content):
    if Title == u'今日已签到':
        return 0
    Sender = {
        'Addr': '****@****.***',
        'Host': 'smtp.****.***',
        'User': '****@****.***',
        'Pass': '********'
    }
    SendTo = ['****@****.****']
    Message = MIMEText(Content, _subtype='plain', _charset='gb2312')
    Message['Subject'] = Title
    Message['From'] = Sender['Addr']
    Message['To'] = ';'.join(SendTo)
    try:
        server = smtplib.SMTP()
        server.connect(Sender['Host'])
        server.login(Sender['User'], Sender['Pass'])
        server.sendmail(Sender['Addr'], SendTo, Message.as_string())
        server.close()
        return 1
    except Exception, e:
        logging.warn(str(e))
        return -1


if __name__ == '__main__':
    logging.info('=' * 50)
    [Result, Info, Detail] = Register()
    SendResult = SendMail(Detail, Info.decode('utf-8'))
    if SendResult == 1:
        logging.info('邮件已发送')
    elif SendResult == -1:
        logging.info('邮件发送失败')
    else:
        logging.info('取消发送')
