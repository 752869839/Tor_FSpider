# -*- coding: utf-8 -*-
import re
import os
import json
import random
import cairosvg
import pymysql
import requests
from lxml import etree
from login.chaojiying import Chaojiying_Client
from login.connecting import conn
from login.config import table,cookie_table
from taskmanage.settings import logger

num = []
class Login(object):
    def __init__(self):
        self.session = self.r_session()
        self.headers = self.r_headers()
        self.url = self.r_url()
        self.login_url = self.login_url()
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
            'Host': 'alibaba2kw6qoh6o.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers


    def r_url(self):
        url = 'http://alibaba2kw6qoh6o.onion/'
        return url

    def login_url(self):
        login_url = 'http://alibaba2kw6qoh6o.onion/login'
        return login_url

    def r_proxies(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()  # 创建游标对象
        cursor.execute("SELECT proxy FROM {} where project_name='Alibaba'".format(table))
        PROXIES = json.loads(cursor.fetchone()[0])
        conn.commit()
        cursor.close()
        conn.close()
        proxie = random.choice(PROXIES)
        proxies = {'http' : proxie}
        return proxies

    def r_get(self):
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info(r.status_code)
        res = etree.HTML(r.text)
        captcha_url = res.xpath('//img[@style="float:right"]/@src')[0].strip().replace("'",'%27')
        logger.info(captcha_url)
        captcha_url = 'http://alibaba2kw6qoh6o.onion' + captcha_url
        logger.info(captcha_url)
        resp = self.session.get(captcha_url,headers=self.headers,proxies=self.proxies)
        # logger.info(resp.text)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open('{}/login/img/alibaba.svg'.format(path), 'w', encoding='utf-8') as f1:
            f1.write(resp.text)
            f1.close()

        cairosvg.svg2png(file_obj=open("{}/login/img/alibaba.svg".format(path), "rb"), write_to="{}/login/img/alibaba.png".format(path))
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/img/alibaba.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1004)
        global err
        err = code["pic_id"]
        result = code ["pic_str"].lower()
        logger.info(result)
        if len(result) < 4:
            self.main()
        data = {
            'captcha': result,
        }
        return data

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        logger.info(im_id)

    def r_post(self,data):
        response = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=data)
        logger.info(response.status_code)
        #logger.info(response.text)
        if '会员登录' in response.text:
            captcha_url = re.findall('background: url(.*?) center',response.text)[0].replace("('",'').replace("'", '%27')
            logger.info(captcha_url)
            captcha_url = 'http://alibaba2kw6qoh6o.onion' + captcha_url
            logger.info(captcha_url)
            resp = self.session.get(captcha_url, headers=self.headers, proxies=self.proxies)
            # logger.info(resp.text)
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            with open('{}/login/img/alibaba2.svg'.format(path), 'w', encoding='utf-8') as f1:
                f1.write(resp.text)
                f1.close()
            cairosvg.svg2png(file_obj=open("{}/login/img/alibaba2.svg".format(path), "rb"),write_to="{}/login/img/alibaba2.png".format(path))
            chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
            im = open('{}/login/img/alibaba2.png'.format(path), 'rb').read()
            code = chaojiying.PostPic(im, 1004)
            global err
            err = code["pic_id"]
            result = code["pic_str"].lower()
            logger.info(result)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username,password FROM {} where domain='alibaba2kw6qoh6o.onion'".format(cookie_table))
            acc = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            account = random.choice(acc)
            username = account[0]
            passwords = account[1]
            logger.info(username)
            logger.info(passwords)
            form = {
                'captcha':result,
                'name':username,
                'passwd':passwords
            }
            return username,form
        else :
            self.error()
            self.main()

    def form_post(self,username,form):
        response = self.session.post(self.login_url,headers=self.headers,proxies=self.proxies,data=form)
        logger.info(response.status_code)
        logger.info(response.text)
        if 'Welcome to ' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info(cookies)
            jsonCookies = json.dumps(cookies)
            return username,jsonCookies
            # conn.ping(reconnect=True)
            # cursor = conn.cursor()
            # sql ="update {} SET cookie=%s  WHERE domain='alibaba2kw6qoh6o.onion' ".format(cookie_table)
            # cookies = jsonCookies
            # cursor.execute(sql, [cookies])
            # conn.commit()
            # cursor.close()
            # conn.close()

        else:
            if len(num) <= 4:
                self.error()
                return self.main()
            else:
                jsonCookies = ""
                return username,jsonCookies

    def main(self):
        num.append(1)
        data = self.r_get()
        username,form = self.r_post(data)
        username,jsonCookies = self.form_post(username,form)
        return username,jsonCookies

if __name__ == '__main__':
    l = Login()
    l.main()