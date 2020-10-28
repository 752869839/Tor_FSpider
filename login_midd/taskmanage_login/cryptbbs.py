# -*- coding: utf-8 -*-
import os
import re
import json
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
        self.headers2 = self.r_headers2()
        self.url = self.r_url()
        self.proxies = self.r_proxies()

    def r_session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        return session

    def r_headers(self):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'cryptbb2gezhohku.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers
    
    
    def r_headers2(self):
        headers2 = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'cryptbb2gezhohku.onion',
            'Connection': 'close',
            'Referer': 'http://cryptbb2gezhohku.onion/',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers2

    def r_url(self):
        url = 'http://cryptbb2gezhohku.onion/member.php?action=login'
        return url

    def r_proxies(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()  # 创建游标对象
        cursor.execute("SELECT proxy FROM {} where project_name='Cryptbbs'".format(table))
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
        url_code = re.findall(r'<img src="(.*?)" alt=', r.text)[0]
        res = self.session.get(url_code, headers=self.headers2, proxies=self.proxies)
        logger.info(res.status_code)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("{}/login/img/cryptbbs.png".format(path), 'wb').write(res.content)
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/img/cryptbbs.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1007)
        global err
        err = code["pic_id"]
        result = code["pic_str"]
        logger.info(result)
        imagehash = re.findall(r'imagehash=([\s|\S]+)', url_code)[0]
        # print(imagehash)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT username,password FROM {} where domain='cryptbb2gezhohku.onion'".format(cookie_table))
        acc = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        account = random.choice(acc)
        print(account)
        username = account[0]
        password = account[1]
        logger.info(username)
        logger.info(password)
        data = {
            'imagestring': result,
            'imagehash': imagehash,
            'username': username,
            'password': password,
            'remember': 'yes',
            'submit': 'Login',
            'action': 'do_login',
            'url': '	http://cryptbb2gezhohku.onion/'
        }
        return username,data

    def r_second(self,username,data):
        response = self.session.post(self.url, headers=self.headers, proxies=self.proxies, data=data)
        logger.info(response.status_code)
        # print(response.text)
        if 'Welcome back,' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            return username,jsonCookies
            # conn = pymysql.connect(host=host, user=user, password=password, database=database)  # 连接mysql数据库
            # cursor = conn.cursor()  # 创建游标对象
            # sql = "insert into cryptbbs(cookies) values (%s);"
            # cookies = jsonCookies
            # cursor.execute(sql, [cookies])
            # conn.commit()  # 提交
            # cursor.close()
            # conn.close()
        else:
            if len(num) <= 2:
                self.error()
                return self.main()
            else:
                jsonCookies = ""
                return username,jsonCookies

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)


    def main(self):
        num.append(1)
        username,data = self.r_first()
        username, jsonCookies = self.r_second(username,data)
        return username,jsonCookies


if __name__ == '__main__':
    l = Login()
    l.main()
