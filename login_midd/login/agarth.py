# -*- coding: utf-8 -*-
import os
import re
import json
import base64
import random
import requests
from chaojiying import Chaojiying_Client
from config import PROXIES,conn,cookie_table

class Login(object):
    def __init__(self):
        self.session = self.r_session()
        self.headers = self.r_headers()
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
            'Host': 'agarthaangodtcz3.onion',
            'Connection': 'keep-alive',
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
        proxies = random.choice(PROXIES)
        return proxies

    def r_first(self):
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        print(r.status_code)
        url_code = re.findall(r'<img src="data:image/jpeg;base64,(.*?)" />', r.text)[0]
        print(url_code)
        agtoken = re.findall(r"<input type='hidden' name='agtoken' value='(.*?)' />", r.text)[0]
        print(agtoken)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("{}/login/code/agarth.png".format(path), 'wb').write(base64.b64decode(url_code))
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/code/agarth.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1006)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        print(result)
        global data
        data = {
                    "agtoken": agtoken, "username": 'wahaha', "password": 'laoganma',
                              "captcha": result, "login": "Login"}

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)

    def r_second(self):
        response = self.session.post(self.url2,headers=self.headers,proxies=self.proxies,data=data)
        print(response.status_code)
        # print(response.text)
        if 'Logout' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='agarthaangodtcz3.onion' ".format(cookie_table)
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

if __name__ == '__main__':
    l = Login()
    l.main()