# -*- coding: utf-8 -*-
import re
import json
import random
import pymysql
import requests
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
            'Host': 'avengersdutyk3xf.onion',
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
            'Host': 'avengersdutyk3xf.onion',
            'Connection': 'close',
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
        conn.ping(reconnect=True)
        cursor = conn.cursor()  # 创建游标对象
        cursor.execute("SELECT proxy FROM {} where project_name='Avenger'".format(table))
        PROXIES = json.loads(cursor.fetchone()[0])
        conn.commit()
        cursor.close()
        conn.close()
        proxie = random.choice(PROXIES)
        proxies = {'http' : proxie}
        return proxies

    def r_first(self):
        res = self.session.get(self.url, headers=self.headers, proxies=self.proxies)
        logger.info(res.status_code)
        my_post_key = re.findall(r'<input name="my_post_key" type="hidden" value="(.*?)" />', res.text)[0]
        # print(my_post_key)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT username,password FROM {} where domain='avengersdutyk3xf.onion'".format(cookie_table))
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
            "action": "do_login", "url": "/index.php", "my_post_key": my_post_key,
            "username": username, "password": password, "remember": "yes"}
        return username,data

    def r_second(self,username,data):
        response = self.session.post(self.url2, headers=self.headers2, proxies=self.proxies, data=data)
        logger.info(response.status_code)
        if 'Log Out' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            return username,jsonCookies
            # conn = pymysql.connect(host=host, user=user, password=password, database=database)  # 连接mysql数据库
            # cursor = conn.cursor()  # 创建游标对象
            # sql = "insert into avenger(cookies) values (%s);"
            # cookies = jsonCookies
            # cursor.execute(sql, [cookies])
            # conn.commit()  # 提交
            # cursor.close()
            # conn.close()
        else:
            if len(num) <= 2:
                return self.main()
            else:
                jsonCookies = ""
                return username,jsonCookies

    def main(self):
        num.append(1)
        username,data = self.r_first()
        username,jsonCookies = self.r_second(username,data)
        return username,jsonCookies


if __name__ == '__main__':
    l = Login()
    l.main()
