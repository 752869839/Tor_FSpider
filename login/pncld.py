# -*- coding: utf-8 -*-
import os
import re
import json
import time
import base64
import random
import requests
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import conn,table,cookie_table
from login.log_decorator import _logger, exception_logger

logger = _logger()
count = []
class PncldLogin(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.url = self.url()
        self.url2 = self.url2()
        self.url_verify = self.verify()
        self.proxies = self.proxies()

    def session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        logger.info('任务获取成功,准备登录')
        return session

    def headers(self):
        headers = {
            'Host': 'pncldyerk4gqofhp.onion',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        return headers

    def url(self):
        url = 'http://pncldyerk4gqofhp.onion/'
        return url

    def url2(self):
        url2 = "http://pncldyerk4gqofhp.onion/free/member.php"
        return url2

    def verify(self):
        url_verify = 'http://pncldyerk4gqofhp.onion/verify'
        return url_verify

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
        r = self.session.get(self.url, headers=self.headers, proxies=self.proxies)
        logger.info('访问登录网址:')
        logger.info(r.status_code)
        time.sleep(3)
        res = self.session.get(self.url, headers=self.headers, proxies=self.proxies)
        logger.info('再放访问该登录网址:')
        logger.info(r.status_code)
        url_code = re.findall(r'<img src="data:image/gif;base64,(.*?)" width="150"', res.text)[0]
        logger.info('获取验证码的base64码')
        logger.info(url_code)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("{}/login/code/pncld.png".format(path), 'wb').write(base64.b64decode(url_code))
        # open("/code/tor_spider/img/pncld.png", 'wb').write(base64.b64decode(url_code))
        im = open('{}/login/code/pncld.png'.format(path), 'rb').read()
        # im = open('/code/tor_spider/img/pncld.png', 'rb').read()
        chaojiying = Chaojiying_Client()
        code = chaojiying.PostPic(im, 1006)
        global err
        err = code["pic_id"]
        result = code["pic_str"]
        results = result.lower()
        logger.info('验证码识别结果为:')
        logger.info(result)
        challenge = re.findall(r'name="challenge" value="(.*?)"><', res.text)[0]
        logger.info('获取challenge:')
        logger.info(challenge)
        form = {
            'captcha': results,
            'challenge': challenge,
            'location': 'A',
            'action': 'do_cap',
            'url': '/403.html'
        }
        return form

    def second(self,form):
        try:
            resp = self.session.post(self.url_verify, headers=self.headers, data=form, proxies=self.proxies)
            logger.info('提交验证码表单:')
            logger.info(resp.status_code)
            my_post_key = re.findall(r'"my_post_key" type="hidden" value="(.*?)" /> <table', resp.text)[0]
            logger.info('获取my_post_key:')
            logger.info(my_post_key)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username,password FROM {} where domain='pncldyerk4gqofhp.onion'".format(
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
                'action': 'do_login',
                'url': "/free/index.php",
                'my_post_key': my_post_key,
                'username': username,
                'password': password,
            }
            return data
        except:
            self.main()

    def third(self,data):
        resp = self.session.post(self.url2, headers=self.headers, data=data, proxies=self.proxies)
        logger.info('请求提交登录表单:')
        logger.info(resp.status_code)
        response = self.session.get(self.url2, headers=self.headers, proxies=self.proxies)
        logger.info('请求主页地址:')
        logger.info(response.status_code)
        if '歡迎您回來' in response.text:
            logger.info('登录成功!!!')
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info('Cookie值:')
            logger.info(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='pncldyerk4gqofhp.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            conn.commit()
            cursor.close()
            conn.close()
            logger.info('Cookie入库完毕,准备采集!')
            return jsonCookies
        else:
            if len(count) <= 3:
                self.error()
                return self.main()

    def error(self):
        chaojiying = Chaojiying_Client()
        im_id = chaojiying.ReportError(err)
        print(im_id)


    def main(self):
        count.append(1)
        form = self.first()
        data = self.second(form)
        self.third(data)


if __name__ == '__main__':
    l = PncldLogin()
    l.main()