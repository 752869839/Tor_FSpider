# -*- coding: utf-8 -*-
import os
import re
import json
import base64
import random
import requests
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import SOCKS_PROXY,mysql_conn,table,cookie_table
from login.mylog import logger

logger = logger()
count = []
class AgarthLogin(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.url = self.url()
        self.url2 = self.url2()
        self.proxies = self.proxies()

    def session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        logger.info('任务获取成功,准备登录')
        return session

    def headers(self):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'agarthaangodtcz3.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def url(self):
        url = 'http://agarthaangodtcz3.onion'
        return url

    def url2(self):
        url2 = 'http://agarthaangodtcz3.onion/login'
        return url2

    def proxies(self):
        proxy = random.choice(SOCKS_PROXY).replace('socks5','socks5h')
        proxies = {"http":proxy}
        logger.info(f'应用代理ip为:{proxies}')
        return proxies

    def first(self):
        logger.info('开始登录:')
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info(f'状态码:{r.status_code}')
        url_code = re.findall(r'<img src="data:image/jpeg;base64,(.*?)" />', r.text)[0]
        logger.info(f'提取url_code:{url_code}')
        agtoken = re.findall(r"<input type='hidden' name='agtoken' value='(.*?)' />", r.text)[0]
        logger.info(f'提取agtoken:{agtoken}')
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("/code/login/img/agarth.png", 'wb').write(base64.b64decode(url_code))
        im = open('/code/login/img/agarth.png', 'rb').read()
        chaojiying = Chaojiying_Client()
        code = chaojiying.PostPic(im, 1006)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        logger.info(f'验证码识别结果为:{result}')
        mysql_conn.ping(reconnect=True)
        cursor = mysql_conn.cursor()
        cursor.execute(
            "SELECT username,password FROM {} where domain='agarthaangodtcz3.onion'".format(
                cookie_table))
        acc = cursor.fetchall()
        mysql_conn.commit()
        cursor.close()
        mysql_conn.close()
        account = random.choice(acc)
        username = account[0]
        password = account[1]
        logger.info(f'登录用户名:{username}')
        logger.info('登录用户密码:{password}')
        data = {
                    "agtoken": agtoken, "username": username, "password": password,
                              "captcha": result, "login": "Login"}
        return data

    def error(self):
        chaojiying = Chaojiying_Client()
        im_id = chaojiying.ReportError(err)
        print(im_id)

    def second(self,data):
        response = self.session.post(self.url2,headers=self.headers,proxies=self.proxies,data=data)
        logger.info('请求提交登录表单:{response.status_code}')
        if 'Logout' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info('登录成功Cookie值:{cookies}')
            jsonCookies = json.dumps(cookies)
            mysql_conn.ping(reconnect=True)
            cursor = mysql_conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='agarthaangodtcz3.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            mysql_conn.commit()
            cursor.close()
            mysql_conn.close()
            logger.info('Cookie入库完毕,准备采集!')
            return jsonCookies
        else :
            if len(count) <= 3:
                self.error()
                return self.main()

    def main(self):
        count.append(1)
        data = self.first()
        self.second(data)

if __name__ == '__main__':
    l = AgarthLogin()
    l.main()