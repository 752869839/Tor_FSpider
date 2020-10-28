# -*- coding: utf-8 -*-
import json
import random
import pymysql
import requests
from config import PROXIES,conn,cookie_table


class Login(object):
    def __init__(self):
        self.session = self.r_session()
        self.headers = self.r_headers()
        self.url = self.r_url()
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
            'Host': '24hourspkcmd7bvr.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            #'Content-Type': 'multipart/form-data; boundary=---------------------------11313324222905'
        }
        return headers

    def r_url(self):
        url = 'http://24hourspkcmd7bvr.onion/'
        return url

    def r_proxies(self):
        proxies = random.choice(PROXIES)
        return proxies

    def r_first(self):
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        print(r.status_code)
        global code
        code = {
            'tor_key': '24SezAm'
        }

    def r_second(self):
        res = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=code)
        print(res.status_code)


    def r_fourth(self):
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        print(cookies)
        jsonCookies = json.dumps(cookies)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        sql = "update {} SET cookie=%s  WHERE domain='24hourspkcmd7bvr.onion' ".format(cookie_table)
        cursor.execute(sql, [jsonCookies])
        conn.commit()
        cursor.close()
        conn.close()
        return jsonCookies

    def main(self):
        self.r_first()
        self.r_second()
        self.r_fourth()


if __name__ == '__main__':
    l = Login()
    l.main()