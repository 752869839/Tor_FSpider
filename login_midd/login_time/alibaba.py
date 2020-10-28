# -*- coding: utf-8 -*-
import re
import os
import json
import random
import cairosvg
import requests
from lxml import etree
from connecting import conn
from config import table,cookie_table
from chaojiying import Chaojiying_Client

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
        print(r.status_code)
        res = etree.HTML(r.text)
        captcha_url = res.xpath('//img[@style="float:right"]/@src')[0].strip().replace("'",'%27')
        print(captcha_url)
        captcha_url = 'http://alibaba2kw6qoh6o.onion' + captcha_url
        print(captcha_url)
        resp = self.session.get(captcha_url,headers=self.headers,proxies=self.proxies)
        # print(resp.text)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open('{}/login_time/img/alibaba.svg'.format(path), 'w', encoding='utf-8') as f1:
            f1.write(resp.text)
            f1.close()

        cairosvg.svg2png(file_obj=open("{}/login_time/img/alibaba.svg".format(path), "rb"), write_to="{}/login_time/img/alibaba.png".format(path))
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login_time/img/alibaba.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1004)
        global err
        err = code["pic_id"]
        result = code ["pic_str"].lower()
        print(result)
        if len(result) < 4:
            self.main()
        data = {
            'captcha': result,
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
        if '会员登录' in response.text:
            captcha_url = re.findall('background: url(.*?) center',response.text)[0].replace("('",'').replace("'", '%27')
            print(captcha_url)
            captcha_url = 'http://alibaba2kw6qoh6o.onion' + captcha_url
            print(captcha_url)
            resp = self.session.get(captcha_url, headers=self.headers, proxies=self.proxies)
            # print(resp.text)
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            with open('{}/login_time/img/alibaba2.svg'.format(path), 'w', encoding='utf-8') as f1:
                f1.write(resp.text)
                f1.close()
            cairosvg.svg2png(file_obj=open("{}/login_time/img/alibaba2.svg".format(path), "rb"),write_to="{}/login_time/img/alibaba2.png".format(path))
            chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
            im = open('{}/login_time/img/alibaba2.png'.format(path), 'rb').read()
            code = chaojiying.PostPic(im, 1004)
            global err
            err = code["pic_id"]
            result = code["pic_str"].lower()
            print(result)
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
            print(username)
            print(passwords)
            form = {
                'captcha':result,
                'name':username,
                'passwd':passwords
            }
            return form
        else :
            self.main()

    def form_post(self,form):
        response = self.session.post(self.login_url,headers=self.headers,proxies=self.proxies,data=form)
        print(response.status_code)
        print(response.text)
        if 'Welcome to ' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='alibaba2kw6qoh6o.onion' ".format(cookie_table)
            print(sql)
            cookies = jsonCookies
            cursor.execute(sql, [cookies])
            conn.commit()
            cursor.close()
            conn.close()
            return jsonCookies

        else:
            if len(num) <= 4:
                # self.error()
                return self.main()
            else:
                jsonCookies = ""
                return jsonCookies

    def main(self):
        num.append(1)
        data = self.r_get()
        form = self.r_post(data)
        jsonCookies = self.form_post(form)
        return jsonCookies

if __name__ == '__main__':
    l = Login()
    l.main()