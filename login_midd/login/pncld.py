# -*- coding: utf-8 -*-
import os
import re
import json
import time
import base64
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
        proxies = {"http": "172.16.30.66:3122"}
        return proxies

    def r_first(self):
        r = self.session.get(self.url, headers=self.headers, proxies=self.proxies)
        print(r.status_code)
        time.sleep(3)
        res = self.session.get(self.url, headers=self.headers, proxies=self.proxies)
        print(res.status_code)
        url_code = re.findall(r'<img src="data:image/gif;base64,(.*?)" width="150"', res.text)[0]
        print(url_code)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("{}/login/code/pncld.png".format(path), 'wb').write(base64.b64decode(url_code))
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/code/pncld.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1006)
        global err
        err = code["pic_id"]
        result = code["pic_str"]
        results = result.lower()
        print(results)
        challenge = re.findall(r'name="challenge" value="(.*?)"><', res.text)[0]
        print(challenge)
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
            print(resp.status_code)
            my_post_key = re.findall(r'"my_post_key" type="hidden" value="(.*?)" /> <table', resp.text)[0]
            print(my_post_key)
            data = {
                'action': 'do_login',
                'url': "/free/index.php",
                'my_post_key': my_post_key,
                'username': 'yuanxiao',
                'password': 'Yanjingxianpi123456789',
            }
            return data
        except:
            self.main()

    def r_third(self,data):
        resp = self.session.post(self.url2, headers=self.headers, data=data, proxies=self.proxies)
        print(resp.status_code)
        response = self.session.get(self.url2, headers=self.headers, proxies=self.proxies)
        print(response.status_code)
        print(response.text)
        if '歡迎您回來' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='pncldyerk4gqofhp.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            conn.commit()
            cursor.close()
            conn.close()
            return jsonCookies
        else:
            self.error()
            self.main()

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)


    def main(self):
        form = self.r_first()
        data = self.r_second(form)
        self.r_third(data)


if __name__ == '__main__':
    l = Login()
    l.main()