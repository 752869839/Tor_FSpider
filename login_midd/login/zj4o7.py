# -*- coding: utf-8 -*-
import os
import re
import json
import time
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
        self.url3 = self.r_url3()
        self.url4 = self.r_url4()
        self.url_code = self.r_code()
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
            'Host': '7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def r_url(self):
        url = 'http://7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion/'
        return url

    def r_url2(self):
        url2 = 'http://7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion/user/login?tpl=def'
        return url2

    def r_url3(self):
        url3 = 'http://7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion/user/login'
        return url3

    def r_url4(self):
        url4 = 'http://7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion/user'
        return url4

    def r_code(self):
        url_code = 'http://7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion/other/vcode4'
        return url_code

    def r_proxies(self):
        proxies = random.choice(PROXIES)
        return proxies

    def r_first(self):
        r = self.session.get(self.url2, headers=self.headers, proxies=self.proxies)
        print(r.status_code)
        res = self.session.get(self.url2,headers=self.headers,proxies=self.proxies)
        print(res.status_code)
        time.sleep(3)
        # print(res.text)
        hash = re.findall(r'name="hash" value="(.*?)" />', res.text)[0]
        print(hash)
        resp = self.session.get(self.url_code,headers=self.headers,proxies=self.proxies)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open( "{}/login/code/zj4o7.png".format(path), 'wb').write(resp.content)
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/code/zj4o7.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1006)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        print(result)
        data = {
            'hash': hash,
            'username': 'wahaha',
            'password': 'laoganma',
            'vcode': result,
        }
        response = self.session.post(self.url3,headers=self.headers,proxies=self.proxies,data=data)
        print(response.status_code)
        print(response.text)
        return data

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)


    def r_second(self,data):
        response = self.session.post(self.url4,headers=self.headers,proxies=self.proxies,data=data)
        print(response.status_code)
        print(response.text)
        if '退出' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            conn.commit()
            cursor.close()
            conn.close()
            return jsonCookies
        else :
            self.error()
            self.main()

    def main(self):
        data = self.r_first()
        self.r_second(data)


if __name__ == '__main__':
    l = Login()
    l.main()