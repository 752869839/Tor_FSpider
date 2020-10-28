# -*- coding: utf-8 -*-
import os
import re
import json
import random
import pymysql
import requests
from chaojiying import Chaojiying_Client
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
            'Host': 'cryptbb2gezhohku.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def r_url(self):
        url = 'http://cryptbb2gezhohku.onion/member.php?action=login'
        return url

    def r_proxies(self):
        proxies = random.choice(PROXIES)
        # proxies = {"http":"47.56.197.233:9398"}
        return proxies

    def r_first(self):
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        print(r.status_code)
        global url_code
        url_code = re.findall(r'<img src="(.*?)" alt=', r.text)[0]
        print(url_code)

    def r_second(self):
        res = self.session.get(url_code,headers=self.headers,proxies=self.proxies)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open( "{}/login/code/cryptbbs.png".format(path), 'wb').write(res.content)
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/code/cryptbbs.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1008)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        print(result)
        imagehash = re.findall(r'imagehash=([\s|\S]+)',url_code)[0]
        print(imagehash)
        global data
        data = {
            'imagestring': result,
            'imagehash':imagehash,
            'username': 'kangshifu',
            'password': 'Kangshifu123456789',
            'remember': 'yes',
            'submit':'Login',
            'action':'do_login',
            'url':'	http://cryptbb2gezhohku.onion/'
        }

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)

    def r_third(self):
        response = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=data)
        print(response.status_code)
        # print(response.text)
        if 'Welcome back,' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='cryptbb2gezhohku.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            conn.commit()
            cursor.close()
            conn.close()
            return jsonCookies
        else :
            self.error()
            self.main()

    def main(self):
        self.r_first()
        self.r_second()
        self.r_third()

if __name__ == '__main__':
    l = Login()
    l.main()