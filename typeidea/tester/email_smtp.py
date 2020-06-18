import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText

a = os.getenv('MY_SMTP_PW')
m = """
你的意见是:    通过    拒绝


紧急处理:    禁止该用户访问本站
"""
smtp_server = 'smtp.163.com'
smtp_passwd = ''
from_addr = 'gai520website@163.com'
to_addr = '643177348@qq.com'
msg = MIMEText(m, 'html', 'utf-8')
msg['Subject'] = Header('新的评论--gai520.com', charset='utf-8')
msg['From'] = 'gai520website@163.com'
msg['To'] = '643177348@qq.com'


def send_email():
    server = smtplib.SMTP(host=smtp_server, port=25)
    server.login(user=from_addr, password=smtp_passwd)
    server.sendmail(from_addr=from_addr, to_addrs=['643177348@qq.com', 'gai520website@163.com'], msg=msg.as_string())


if __name__ == '__main__':
    send_email()
