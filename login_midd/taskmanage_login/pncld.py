# -*- coding: utf-8 -*-
import os
import re
import json
import time
import base64
import random
import pymysql
import requests
from login.chaojiying import Chaojiying_Client
from login.connecting import conn
from login.config import table,cookie_table
from taskmanage.settings import logger


num = []
class Login(object):
    def __init__(self):
        self.session = self.r_session()
        self.headers = self.r_headers()
        self.url = self.r_url()
        self.url2 = self.r_url2()
        self.url_verify = self.r_verify()
        self.proxies = self.r_proxies()

    def r_session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        return session

    def r_headers(self):
        headers = {
            'Host': 'pncldyerk4gqofhp.onion',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        return headers

    def r_url(self):
        url = 'http://pncldyerk4gqofhp.onion/'
        return url

    def r_url2(self):
        url2 = "http://pncldyerk4gqofhp.onion/free/member.php"
        return url2

    def r_verify(self):
        url_verify = 'http://pncldyerk4gqofhp.onion/verify'
        return url_verify

    def r_proxies(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT proxy FROM {} where project_name='Pncld'".format(table))
        PROXIES = json.loads(cursor.fetchone()[0])
        conn.commit()
        cursor.close()
        conn.close()
        proxie = random.choice(PROXIES)
        proxies = {'http' : proxie}
        return proxies


    def r_first(self):
        r = self.session.get(self.url, headers=self.headers, proxies=self.proxies)
        logger.info(r.status_code)
        time.sleep(3)
        res = self.session.get(self.url, headers=self.headers, proxies=self.proxies)
        logger.info(res.status_code)
        url_code = re.findall(r'<img src="data:image/gif;base64,(.*?)" width="150"', res.text)[0]
        logger.info(url_code)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("{}/login/img/pncld.png".format(path), 'wb').write(base64.b64decode(url_code))
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/img/pncld.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1006)
        global err
        err = code["pic_id"]
        result = code["pic_str"]
        results = result.lower()
        logger.info(results)
        challenge = re.findall(r'name="challenge" value="(.*?)"><', res.text)[0]
        logger.info(challenge)
        form = {
            'captcha': results,
            'challenge': challenge,
            'location': 'A',
            'action': 'do_cap',
            'url': '/403.html'
        }
        return form

    def r_second(self,form):
        try:
            resp = self.session.post(self.url_verify, headers=self.headers, data=form, proxies=self.proxies)
            logger.info(resp.status_code)
            my_post_key = re.findall(r'"my_post_key" type="hidden" value="(.*?)" /> <table', resp.text)[0]
            logger.info(my_post_key)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            cursor.execute("SELECT username,password FROM {} where domain='pncldyerk4gqofhp.onion'".format(cookie_table))
            acc = cursor.fetchall()
            logger.info(acc)
            conn.commit()
            cursor.close()
            conn.close()
            account = random.choice(acc)
            logger.info(account)
            username = account[0]
            password = account[1]
            logger.info(username)
            logger.info(password)
            data = {
                'action': 'do_login',
                'url': "/free/index.php",
                'my_post_key': my_post_key,
                'username': username,
                'password': password,
            }
            resp = self.session.post(self.url2, headers=self.headers, data=data, proxies=self.proxies)
            logger.info(resp.status_code)
            return username
        except:
            self.main()

    def r_third(self,username):
        response = self.session.get(self.url2, headers=self.headers, proxies=self.proxies)
        logger.info(response.status_code)
        if '歡迎您回來' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info(cookies)
            jsonCookies = json.dumps(cookies)
            # conn.ping(reconnect=True)
            # cursor = conn.cursor()
            # sql = "insert into pncld(cookies) values (%s);"
            # cookies = jsonCookies
            # cursor.execute(sql, [cookies])
            # conn.commit()
            # cursor.close()
            # conn.close()
            return username,jsonCookies
        else:
            if len(num) <= 3:
                self.error()
                return self.main()
            else:
                jsonCookies = ""
                return username, jsonCookies

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        logger.info(im_id)


    def main(self):
        form = self.r_first()
        username = self.r_second(form)
        username,jsonCookies = self.r_third(username)
        return username,jsonCookies


if __name__ == '__main__':
    l = Login()
    l.main()
