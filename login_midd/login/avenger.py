# -*- coding: utf-8 -*-
import re
import json
import random
import pymysql
import requests
from config import PROXIES,conn,cookie_table

class Login(object):
    def __init__(self):
        self.session = self.r_session()
        self.headers = self.r_headers()
        self.headers2 = self.r_headers2()
        self.url = self.r_url()
        self.url2 = self.r_url2()
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
            'Host': 'avengersdutyk3xf.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def r_headers2(self):
        headers2 = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'avengersdutyk3xf.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'http://avengersdutyk3xf.onion/'
        }
        return headers2

    def r_url(self):
        url = 'http://avengersdutyk3xf.onion'
        return url

    def r_url2(self):
        url2 = 'http://avengersdutyk3xf.onion/member.php'
        return url2

    def r_proxies(self):
        proxies = random.choice(PROXIES)
        return proxies

    def r_first(self):
        res = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        print(res.status_code)
        my_post_key = re.findall(r'<input name="my_post_key" type="hidden" value="(.*?)" />', res.text)[0]
        print(my_post_key)
        global data
        data = {
            "action": "do_login", "url": "/index.php", "my_post_key": my_post_key,
                      "username": 'laoganma', "password": "Laoganma123", "remember": "yes"}

    def r_second(self):
        response = self.session.post(self.url2,headers=self.headers2,proxies=self.proxies,data=data)
        print(response.text)
        if 'Log Out' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='avengersdutyk3xf.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            conn.commit()
            cursor.close()
            conn.close()
            return jsonCookies
        else :
            self.main()

    def main(self):
        self.r_first()
        self.r_second()

if __name__ == '__main__':
    l = Login()
    l.main()