# coding=gbk
# 爬取逆天邪神最新章节并发送邮件
import urllib.request
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import ssl
# 加入ssl验证
ssl._create_default_https_context = ssl._create_unverified_context


def send_mail(title, article, receiver):
    host = 'smtp.qq.com'  # QQ邮箱SMTP服务器的host
    user = 'xxxxxxxx@qq.com'  # 邮件地址
    password = 'xxxxxxxxx'  # 邮箱授权码，注意不是qq邮箱的密码
    sender = user
    coding = 'utf8'
    message = MIMEText(article, 'plain', coding)
    message['From'] = Header(sender, coding)
    message['To'] = Header(receiver, coding)
    message['subject'] = Header(title, coding)

    try:
        mail_client = smtplib.SMTP_SSL(host, 465)  # 部分邮箱信道不同，又有可能没有开启SSL服务，具体查询
        mail_client.connect(host)
        mail_client.login(user, password)
        mail_client.sendmail(sender, receiver, message.as_string())
        mail_client.close()
        print('邮件已成功发送给:' + receiver)
    except:
        print('发送失败!')


def main():
    chapter = 1688
    while True:
        localtime = time.asctime(time.localtime(time.time()))  # 报时，免得程序卡住不知道～
        print("程序运行中，正在获取更新，当前时间：", localtime)
        url = 'https://www.booktxt.net/2_2221/'
        headers = {'User-Agent': 'Mozilla/5.0 3578.98 Safari/537.36'}  # 添加headers防止官网认为是爬虫而屏蔽访问
        req = urllib.request.Request(url, headers=headers)
        try:
            rsp = urllib.request.urlopen(req)
            # print('rsp:', rsp)
        except:
            continue
        html = rsp.read().decode('GBK', 'ignore')

        html = BeautifulSoup(html, 'html.parser')
        for link in html.find_all('a'):
            info_link = link.get('href')
            info_text = link.get_text(strip=True)
            # print(info_link)
            if '.html' in info_link:
                # 获取章节数字
                next_chapter = filter(str.isdigit, info_text)
                next_chapter = int("".join(list(next_chapter)))
                if next_chapter > chapter:
                    print("---------------------------")
                    print('最新章节：' + info_text)
                    print(url+info_link)
                    send_mail(info_text, url + info_link, 'xxxxxxx')  # 填入需要接受邮件的邮箱
                    print('逆天邪神已更新,更新时间:', localtime)
                    print("---------------------------")
                    # send email
                    chapter = next_chapter
                    # 更新一章之后休息两小时
                    time.sleep(7200)
                print("-----------未更新------------")
                break
        time.sleep(60)  # 数字决定几秒爬取一次


if __name__ == '__main__':
    main()
