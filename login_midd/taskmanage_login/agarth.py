# -*- coding: utf-8 -*-
import os
import re
import json
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
            'Host': 'agarthaangodtcz3.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def r_url(self):
        url = 'http://agarthaangodtcz3.onion'
        return url

    def r_url2(self):
        url2 = 'http://agarthaangodtcz3.onion/login'
        return url2

    def r_proxies(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT proxy FROM {} where project_name='Agarth'".format(table))
        PROXIES = json.loads(cursor.fetchone()[0])
        conn.commit()
        cursor.close()
        conn.close()
        proxie = random.choice(PROXIES)
        proxies = {'http' : proxie}
        return proxies


    def r_first(self):
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info(r.status_code)
        url_code = re.findall(r'<img src="data:image/jpeg;base64,(.*?)" />', r.text)[0]
        #print(url_code)
        agtoken = re.findall(r"<input type='hidden' name='agtoken' value='(.*?)' />", r.text)[0]
        #print(agtoken)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("{}/login/img/agarth.png".format(path), 'wb').write(base64.b64decode(url_code))
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/img/agarth.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1006)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        logger.info(result)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT username,password FROM {} where domain='agarthaangodtcz3.onion'".format(cookie_table))
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
                    "agtoken": agtoken, "username": username, "password": password,
                              "captcha": result, "login": "Login"}
        return username , data

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)

    def r_second(self,username,data):
        response = self.session.post(self.url2,headers=self.headers,proxies=self.proxies,data=data)
        logger.info(response.status_code)

        if 'Logout' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            return username,jsonCookies
            # conn = pymysql.connect(host=host, user=user, password=password, database=database)  # 连接mysql数据库
            # cursor = conn.cursor()
            # sql = "insert into agarth(cookies) values (%s);"
            # cookies = jsonCookies
            # cursor.execute(sql, [cookies])
            # conn.commit()
            # cursor.close()
            # conn.close()
        else:
            if len(num) <= 2:
                self.error()
                return self.main()
            else:
                jsonCookies = ""
                return username,jsonCookies

    def main(self):
        num.append(1)
        username,data = self.r_first()
        username,jsonCookies = self.r_second(username,data)
        return username,jsonCookies

if __name__ == '__main__':
    l = Login()
    l.main()
