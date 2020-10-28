# -*- coding: utf-8 -*-
import os
import json
import random
import pymysql
import requests
from datetime import datetime
from chaojiying import Chaojiying_Client
from connecting import conn
from config import table,cookie_table

num = []
class Login(object):
    def __init__(self):
        self.session = self.r_session()
        self.headers = self.r_headers()
        self.headers2 = self.r_headers2()
        self.url = self.r_url()
        self.url_code = self.r_url_code()
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
            'Host': 'apollonvm7uin7yw.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def r_headers2(self):
        headers2 = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'apollonvm7uin7yw.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'http://apollonvm7uin7yw.onion/login.php',
        }
        return headers2

    def r_url(self):
        url = 'http://apollonvm7uin7yw.onion/login.php'
        return url

    def r_url_code(self):
        url_code = 'http://apollonvm7uin7yw.onion/cap/capshow.php'
        return url_code

    def r_proxies(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT proxy FROM {} where project_name='Apollo'".format(table))
        PROXIES = json.loads(cursor.fetchone()[0])
        conn.commit()
        cursor.close()
        conn.close()
        proxie = random.choice(PROXIES)
        proxies = {'http' : proxie}
        return proxies

    def r_first(self):
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        print(r.status_code)
        res = self.session.get(self.url_code,headers=self.headers2,proxies=self.proxies)
        print(res.status_code)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open( "{}/login_time/img/apollo.png".format(path), 'wb').write(res.content)
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login_time/img/apollo.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1008)
        global err
        err = code["pic_id"]
        result = code ["pic_str"].lower()
        print(result)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT username,password FROM {} where domain='apollonvm7uin7yw.onion'".format(cookie_table))
        acc = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        account = random.choice(acc)
        print(account)
        username = account[0]
        password = account[1]
        print(username)
        print(password)
        data = {
            'capt_code': result,
            'l_username': username,
            'l_password': password,
        }
        return username,data

    def r_second(self,username,data):
        response = self.session.post(self.url, headers=self.headers2, proxies=self.proxies, data=data)
        print(response.status_code)
        if 'Welcome Back,' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            gmt_modified = datetime.utcnow()
            sql = "update {} SET cookie=%s , gmt_modified=%s WHERE domain='apollonvm7uin7yw.onion' and username=%s".format(cookie_table)
            print(sql)
            cookies = jsonCookies
            cursor.execute(sql, [cookies,gmt_modified,username])
            conn.commit()
            cursor.close()
            conn.close()
            return username,jsonCookies
        else:
            if len(num) <= 5:
                # self.error()
                return self.main()
            else:
                jsonCookies = ""
                return username,jsonCookies

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)


    def main(self):
        num.append(1)
        username,data = self.r_first()
        username,jsonCookies = self.r_second(username,data)
        return username,jsonCookies

if __name__ == '__main__':
    l = Login()
    l.main()
