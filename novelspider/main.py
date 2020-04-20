# coding=gbk
# ��ȡ����а�������½ڲ������ʼ�
import urllib.request
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import ssl
# ����ssl��֤
ssl._create_default_https_context = ssl._create_unverified_context


def send_mail(title, article, receiver):
    host = 'smtp.qq.com'  # QQ����SMTP��������host
    user = 'xxxxxxxx@qq.com'  # �ʼ���ַ
    password = 'xxxxxxxxx'  # ������Ȩ�룬ע�ⲻ��qq���������
    sender = user
    coding = 'utf8'
    message = MIMEText(article, 'plain', coding)
    message['From'] = Header(sender, coding)
    message['To'] = Header(receiver, coding)
    message['subject'] = Header(title, coding)

    try:
        mail_client = smtplib.SMTP_SSL(host, 465)  # ���������ŵ���ͬ�����п���û�п���SSL���񣬾����ѯ
        mail_client.connect(host)
        mail_client.login(user, password)
        mail_client.sendmail(sender, receiver, message.as_string())
        mail_client.close()
        print('�ʼ��ѳɹ����͸�:' + receiver)
    except:
        print('����ʧ��!')


def main():
    chapter = 1688
    while True:
        localtime = time.asctime(time.localtime(time.time()))  # ��ʱ����ó���ס��֪����
        print("���������У����ڻ�ȡ���£���ǰʱ�䣺", localtime)
        url = 'https://www.booktxt.net/2_2221/'
        headers = {'User-Agent': 'Mozilla/5.0 3578.98 Safari/537.36'}  # ���headers��ֹ������Ϊ����������η���
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
                # ��ȡ�½�����
                next_chapter = filter(str.isdigit, info_text)
                next_chapter = int("".join(list(next_chapter)))
                if next_chapter > chapter:
                    print("---------------------------")
                    print('�����½ڣ�' + info_text)
                    print(url+info_link)
                    send_mail(info_text, url + info_link, 'xxxxxxx')  # ������Ҫ�����ʼ�������
                    print('����а���Ѹ���,����ʱ��:', localtime)
                    print("---------------------------")
                    # send email
                    chapter = next_chapter
                    # ����һ��֮����Ϣ��Сʱ
                    time.sleep(7200)
                print("-----------δ����------------")
                break
        time.sleep(60)  # ���־���������ȡһ��


if __name__ == '__main__':
    main()
