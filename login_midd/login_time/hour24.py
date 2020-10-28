# -*- coding: utf-8 -*-
import re
import json
import random
import pymysql
import requests
from datetime import datetime
from connecting import conn
from config import table,cookie_table

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
        print("{}".format(r.status_code))
        global code
        code = {
            'tor_key': '24SezAm'
        }
        res = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=code)
        print(res.status_code)

    def r_second(self):
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        print(cookies)
        jsonCookies = json.dumps(cookies)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        username = 'wahaha@qq.com'
        gmt_modified = datetime.utcnow()
        sql = "update {} SET cookie=%s , gmt_modified=%s WHERE domain='24hourspkcmd7bvr.onion' and username=%s".format(cookie_table)
        cookies = jsonCookies
        cursor.execute(sql, [cookies, gmt_modified, username])
        conn.commit()
        cursor.close()
        conn.close()
        return username, jsonCookies

    def main(self):
        self.r_first()
        username, jsonCookies = self.r_second()
        return username,jsonCookies


if __name__ == '__main__':
    l = Login()
    l.main()
