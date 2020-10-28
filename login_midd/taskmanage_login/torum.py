# -*- coding: utf-8 -*-
import os
import re
import json
import random
import pymysql
import requests
from login.chaojiying import Chaojiying_Client
from login.connecting import conn
from login.config import table,cookie_table
from taskmanage.settings import logger

num = []
class Login(object):
    def __init__(self):
        self.session = self.r_session()
        self.headers = self.r_headers()
        self.headers2 = self.r_headers2()
        self.url = self.r_url()
        self.url2 = self.r_url2()
        self.url3 = self.r_url3()
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
            'Host': 'torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion',
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
            'Host': 'torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion',
            'Connection': 'close',
            'Referer': 'http://torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion/',
            'Upgrade-Insecure-Requests': '1',
                        }
        return headers2

    def r_url(self):
        url = 'http://torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion/captcha/'
        return url

    def r_url2(self):
        url2 = 'http://torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion/'
        return url2

    def r_url3(self):
        url3 = 'http://torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion/ucp.php?mode=login'
        return url3

    def r_url_code(self):
        url_code = 'http://torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion/captcha/image.php'
        return url_code

    def r_proxies(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT proxy FROM {} where project_name='Torum'".format(table))
        PROXIES = json.loads(cursor.fetchone()[0])
        conn.commit()
        cursor.close()
        conn.close()
        proxie = random.choice(PROXIES)
        proxies = {'http' : proxie}
        return proxies


    def r_first(self):
        r = self.session.get(self.url_code, headers=self.headers, proxies=self.proxies)
        logger.info(r.status_code)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("{}/login/img/torum.png".format(path), 'wb').write(r.content)
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/img/torum.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1902)
        global err
        err = code["pic_id"]
        result = code["pic_str"].lower()
        print(result)
        co = {
            'input': result,
            'submit': 'Verify'
        }
        res = self.session.post(self.url, headers=self.headers, proxies=self.proxies, data=co)
        logger.info(res.status_code)

    def r_second(self):
        resp = self.session.get(self.url2, headers=self.headers, proxies=self.proxies)
        logger.info(resp.status_code)
        sid = re.findall(r'<dd><input type="hidden" name="sid" value="(.*?)" />', resp.text)[0]
        print(sid)
        creation_time = re.findall(r'<input type="hidden" name="creation_time" value="(.*?)" />', resp.text)[0]
        print(creation_time)
        form_token = re.findall(r'<input type="hidden" name="form_token" value="(.*?)" />', resp.text)[0]
        print(form_token)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username,password FROM {} where domain='torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion'".format(
                cookie_table))
        acc = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        account = random.choice(acc)
        print(account)
        username = account[0]
        password = account[1]
        logger.info(username)
        logger.info(password)
        data = {
            'sid': sid,
            'creation_time': creation_time,
            'form_token': form_token,
            'username': username,
            'password': password,
            'redirect': './index.php?',
            'login': 'Login',

        }
        return username,data

    def r_third(self,username,data):
        response = self.session.post(self.url3, headers=self.headers2, proxies=self.proxies, data=data)
        print(response.status_code)
        if 'Beginners Lounge' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            return username,jsonCookies
            # conn = pymysql.connect(host=host, user=user, password=password, database=database)  # 连接mysql数据库
            # cursor = conn.cursor()
            # sql = "insert into torum(cookies) values (%s);"
            # cookies = jsonCookies
            # cursor.execute(sql, [cookies])
            # conn.commit()
            # cursor.close()
            # conn.close()
        else:
            if len(num) <= 2:
                self.error()
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
        self.r_first()
        username, data = self.r_second()
        username,jsonCookies = self.r_third(username,data)
        return username,jsonCookies

if __name__ == '__main__':
    l = Login()
    l.main()
