# -*- coding: utf-8 -*-
import os
import re
import json
import random
import requests
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import conn,table,cookie_table
from login.log_decorator import _logger, exception_logger

logger = _logger()
count = []
class CryptbbsLogin(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.url = self.url()
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
            'Host': 'cryptbb2gezhohku.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def url(self):
        url = 'http://cryptbb2gezhohku.onion/member.php?action=login'
        return url

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
        url_code = re.findall(r'<img src="(.*?)" alt=', r.text)[0]
        logger.info('提取url_code:')
        logger.info(url_code)
        res = self.session.get(url_code,headers=self.headers,proxies=self.proxies)
        logger.info('访问验证码链接:')
        logger.info(res.status_code)
        imagehash = re.findall(r'imagehash=([\s|\S]+)',url_code)[0]
        logger.info('提取imagehash:')
        logger.info(imagehash)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open( "{}/login/code/cryptbbs.png".format(path), 'wb').write(res.content)
        # open( "/code/tor_spider/img/cryptbbs.png", 'wb').write(res.content)
        im = open('{}/login/code/cryptbbs.png'.format(path), 'rb').read()
        # im = open('/code/tor_spider/img/cryptbbs.png', 'rb').read()
        chaojiying = Chaojiying_Client()
        code = chaojiying.PostPic(im, 1008)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        logger.info('验证码识别结果为:')
        logger.info(result)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username,password FROM {} where domain='cryptbb2gezhohku.onion'".format(
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
            'imagestring': result,
            'imagehash':imagehash,
            'username': username,
            'password': password,
            'remember': 'yes',
            'submit':'Login',
            'action':'do_login',
            'url':'	http://cryptbb2gezhohku.onion/'
        }
        return data

    def second(self,data):
        response = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=data)
        logger.info('请求提交登录表单:')
        logger.info(response.status_code)
        if 'Welcome back,' in response.text:
            logger.info('登录成功!!!')
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info('Cookie值:')
            logger.info(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='cryptbb2gezhohku.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            conn.commit()
            cursor.close()
            conn.close()
            logger.info('Cookie入库完毕,准备采集!')
            return jsonCookies
        else :
            if len(count) <= 3:
                self.error()
                return self.main()

    def error(self):
        chaojiying = Chaojiying_Client()
        im_id = chaojiying.ReportError(err)
        print(im_id)


    def main(self):
        count.append(1)
        data = self.first()
        self.second(data)

if __name__ == '__main__':
    l = CryptbbsLogin()
    l.main()