# -*- coding: utf-8 -*-
import re
import os
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
        self.proxies = self.r_proxies()

    def r_session(self):
        session = requests.session()
        return session

    def r_headers(self):
        headers = {
        "User-Agent":'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.5',
        'Host': 'gw6zzvqgy6v2czxrmphuerrtbirftvkyfkeoaiorg5qijqlsbqfpqjqd.onion',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests': '1' ,
        }
        return headers

    def r_url(self):
        url = 'http://gw6zzvqgy6v2czxrmphuerrtbirftvkyfkeoaiorg5qijqlsbqfpqjqd.onion/user/login'
        return url


    def r_proxies(self):
        proxies = random.choice(PROXIES)
        return proxies

    def r_first(self):
        res = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        print(res.status_code)
        url_code = re.findall(r'base64,(.*?)"..alt=', res.text)[0]
        print(url_code)
        csrftoken = re.findall(r'name="csrfmiddlewaretoken" value="(.*?)">', res.text)[0]
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open( "{}/login/code/gw6zz.png".format(path), 'wb').write(base64.b64decode(url_code))
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/code/gw6zz.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1006)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        print(result)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username,password FROM {} where domain='gw6zzvqgy6v2czxrmphuerrtbirftvkyfkeoaiorg5qijqlsbqfpqjqd.onion'".format(cookie_table))
        acc = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        account = random.choice(acc)
        username = account[0]
        passwords = account[1]
        data = {
            "csrfmiddlewaretoken":csrftoken,"captcha_code": result,"username": username, "password": passwords
        }
        return data


    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)

    def r_second(self,data):
        response = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=data)
        print(response.status_code)
        # print(response.text)
        if '激活权限.' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='gw6zzvqgy6v2czxrmphuerrtbirftvkyfkeoaiorg5qijqlsbqfpqjqd.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            conn.commit()
            cursor.close()
            conn.close()
            return jsonCookies
        else :
            self.error()
            self.main()

    def main(self):
        form = self.r_first()
        self.r_second(form)


if __name__ == '__main__':
    l = Login()
    l.main()