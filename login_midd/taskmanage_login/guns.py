# -*- coding: utf-8 -*-
import os
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
        self.url = self.r_url()
        self.url_code = self.r_url_code()
        self.proxies = self.r_proxies()

    def r_session(self):
        session = requests.session()
        return session

    def r_headers(self):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'gunsganos2raowan5y2nkblujnmza32v2cwkdgy6okciskzabchx4iqd.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers


    def r_url(self):
        url = 'http://gunsganos2raowan5y2nkblujnmza32v2cwkdgy6okciskzabchx4iqd.onion/login.php'
        return url

    def r_url_code(self):
        url_code = 'http://gunsganos2raowan5y2nkblujnmza32v2cwkdgy6okciskzabchx4iqd.onion/securimage-master/securimage_show.php'
        return url_code

    def r_proxies(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT proxy FROM {} where project_name='tor_spider'".format(table))
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
        res = self.session.get(self.url_code,headers=self.headers,proxies=self.proxies)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open( "{}/login/img/guns.png".format(path), 'wb').write(res.content)
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/img/guns.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1008)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        logger.info(result)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username,password FROM {} where domain='gunsganos2raowan5y2nkblujnmza32v2cwkdgy6okciskzabchx4iqd.onion'".format(cookie_table))
        acc = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        account = random.choice(acc)
        username = account[0]
        passwords = account[1]
        data = {
            'captcha_code': result,
            'username': username,
            'password': passwords,
        }
        return username,data

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        logger.info(im_id)

    def r_second(self,username,data):
        response = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=data)
        logger.info(response.status_code)
        # logger.info(response.text)
        if 'Home' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info(cookies)
            jsonCookies = json.dumps(cookies)
            return username,jsonCookies
        else:
            if len(num) <= 4:
                self.error()
                return self.main()
            else:
                jsonCookies = ""
                return username, jsonCookies

    def main(self):
        num.append(1)
        username,data = self.r_first()
        username, jsonCookies = self.r_second(username,data)
        return username,jsonCookies

if __name__ == '__main__':
    l = Login()
    l.main()