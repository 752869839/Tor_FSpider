# -*- coding: utf-8 -*-
import os
import re
import json
import random
import requests
from connecting import conn
from config import table,cookie_table
from chaojiying import Chaojiying_Client

num = []
class Login(object):
    def __init__(self):
        self.session = self.r_session()
        self.headers = self.r_headers()
        self.url = self.r_url()
        self.url1 = self.r_url1()
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
            'Host': 'sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def r_url(self):
        url = 'http://sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion/protectd?invita='
        return url

    def r_url1(self):
        url1 = 'http://sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion/?invita='
        return url1

    def r_url2(self):
        url2 = 'http://sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion/site/loginp?invita='
        return url2


    def r_proxies(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT proxy FROM {} where project_name='Sfdu2'".format(table))
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
        rs = self.session.get(self.url1,headers=self.headers,proxies=self.proxies)
        print(rs.status_code)
        res = self.session.get(self.url2,headers=self.headers,proxies=self.proxies)
        csrf = re.findall(r'name="_csrf-f".value="(.*?)">', res.text)[0]
        print(csrf)
        captcha = re.findall(r'id="loginform-verifycode-image".src="(.*?)".alt',res.text)[0]
        print(captcha)
        url_code = 'http://sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion'+captcha
        resp = self.session.get(url_code,headers=self.headers,proxies=self.proxies)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open( "{}/login_time/img/sfdu2.png".format(path), 'wb').write(resp.content)
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login_time/img/sfdu2.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1006)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        print(result)
        username = ['bingning1','bingning2','bingning3','bingning4','bingning5','bingning6','bingning7','bingning8','bingning9','bingning10']
        username = random.choice(username)
        # conn.ping(reconnect=True)
        # cursor = conn.cursor()
        # cursor.execute("SELECT username,password FROM {} where domain='sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion'".format(cookie_table))
        # acc = cursor.fetchall()
        # conn.commit()
        # cursor.close()
        # conn.close()
        # account = random.choice(acc)
        # username = account[0]
        # password = account[1]
        data = {
            '_csrf-f': csrf,
            'LoginForm[username]': username,
            'LoginForm[password]': 'BINGNING',
            'LoginForm[verifyCode]': result,
        }
        return data

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)


    def r_second(self,data):
        response = self.session.post(self.url2,headers=self.headers,proxies=self.proxies,data=data)
        print(response.status_code)
        #print(response.text)
        if '个人中心' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion' ".format(cookie_table)
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
        data = self.r_first()
        jsonCookies = self.r_second(data)
        return jsonCookies


if __name__ == '__main__':
    l = Login()
    l.main()