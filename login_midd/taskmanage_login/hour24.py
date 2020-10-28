# -*- coding: utf-8 -*-
import re
import json
import random
import pymysql
import requests
from taskmanage.settings import logger
from login.connecting import conn
from login.config import table

class Login(object):
    def __init__(self):
        self.session = self.r_session()
        self.headers = self.r_headers()
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
            'Host': '24hourspkcmd7bvr.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
            #'Content-Type': 'multipart/form-data; boundary=---------------------------11313324222905'
        }
        return headers

    def r_url(self):
        url = 'http://24hourspkcmd7bvr.onion/'
        return url


    def r_proxies(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT proxy FROM {} where project_name='Hour24'".format(table))
        PROXIES = json.loads(cursor.fetchone()[0])
        conn.commit()
        cursor.close()
        conn.close()
        proxie = random.choice(PROXIES)
        proxies = {'http' : proxie}
        return proxies


    def r_first(self):
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info("{}".format(r.status_code))
        global code
        code = {
            'tor_key': '24SezAm'
        }
        res = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=code)
        print(res.status_code)

    def r_second(self):
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        print(cookies)
        username = 'wahaha@qq.com'
        jsonCookies = json.dumps(cookies)
        return username,jsonCookies

        # conn = pymysql.connect(host=host, user=user, password=password, database=database)  # 连接mysql数据库
        # cursor = conn.cursor()
        # sql = "insert into hour24(cookies) values (%s);"
        # cookies = jsonCookies
        # cursor.execute(sql, [cookies])
        # conn.commit()
        # cursor.close()
        # conn.close()
        # else :
        #     self.main()

    def main(self):
        self.r_first()
        username, jsonCookies = self.r_second()
        return username,jsonCookies


if __name__ == '__main__':
    l = Login()
    l.main()
