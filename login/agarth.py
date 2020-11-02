# -*- coding: utf-8 -*-
import os
import re
import json
import base64
import random
import requests
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import conn,table,cookie_table
from login.log_decorator import _logger, exception_logger

logger = _logger()

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
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT proxy FROM {} where project_name='tor_spider'".format(table))
        tor_proxy = json.loads(cursor.fetchone()[0])
        conn.commit()
        cursor.close()
        conn.close()
        proxy = random.choice(tor_proxy)
        proxies = {'http' : proxy}
        logger.info('应用代理ip为:')
        logger.info(proxies)
        return proxies

    def first(self):
        logger.info('开始登录:')
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info('访问登录网址:')
        logger.info(r.status_code)
        url_code = re.findall(r'<img src="data:image/jpeg;base64,(.*?)" />', r.text)[0]
        logger.info('提取url_code:')
        logger.info(url_code)
        agtoken = re.findall(r"<input type='hidden' name='agtoken' value='(.*?)' />", r.text)[0]
        logger.info('提取agtoken:')
        logger.info(agtoken)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("{}/login/code/agarth.png".format(path), 'wb').write(base64.b64decode(url_code))
        # open("/code/tor_spider/img/agarth.png", 'wb').write(base64.b64decode(url_code))
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/code/agarth.png'.format(path), 'rb').read()
        # im = open('/code/tor_spider/img/agarth.png', 'rb').read()
        code = chaojiying.PostPic(im, 1006)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        logger.info('验证码识别结果为:')
        logger.info(result)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username,password FROM {} where domain='agarthaangodtcz3.onion'".format(
                cookie_table))
        acc = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        account = random.choice(acc)
        username = account[0]
        password = account[1]
        logger.info('获取登录用户名:')
        logger.info(username)
        logger.info('获取登录用户密码:')
        logger.info(password)
        data = {
                    "agtoken": agtoken, "username": username, "password": password,
                              "captcha": result, "login": "Login"}
        return data

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)

    def second(self,data):
        response = self.session.post(self.url2,headers=self.headers,proxies=self.proxies,data=data)
        logger.info('请求提交登录表单:')
        logger.info(response.status_code)
        if 'Logout' in response.text:
            logger.info('登录成功!!!')
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info('Cookie值:')
            logger.info(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='agarthaangodtcz3.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            conn.commit()
            cursor.close()
            conn.close()
            logger.info('Cookie入库完毕,准备采集!')
            return jsonCookies
        else :
            self.error()
            self.main()

    def main(self):
        data = self.first()
        self.second(data)

if __name__ == '__main__':
    l = AgarthLogin()
    l.main()