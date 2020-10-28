# -*- coding: utf-8 -*-
import os
import json
import random
import requests
from chaojiying import Chaojiying_Client
from config import PROXIES,conn,cookie_table

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
            'Host': 'c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers


    def r_url(self):
        url = 'http://c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion/login'
        return url

    def r_url_code(self):
        url_code = 'http://c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion/jcaptcha.jpg'
        return url_code

    def r_proxies(self):
        proxies = random.choice(PROXIES)
        return proxies

    def r_get(self):
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        print(r.status_code)
        res = self.session.get(self.url_code,headers=self.headers,proxies=self.proxies)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open( "{}/login/code/c2p3h.png".format(path), 'wb').write(res.content)
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/code/c2p3h.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1008)
        global err
        err = code["pic_id"]
        result = code ["pic_str"].lower()
        print(result)
        data = {
            'captcha': result,
            'username': 'nongfu',
            'password': 'shanquan',
        }
        return data

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)

    def r_post(self,data):
        response = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=data)
        print(response.status_code)
        #print(response.text)
        if '您当前为：非 VIP' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            conn.commit()
            cursor.close()
            conn.close()
            return jsonCookies
        else :
            self.error()
            self.main()

    def main(self):
        data = self.r_get()
        self.r_post(data)

if __name__ == '__main__':
    l = Login()
    l.main()