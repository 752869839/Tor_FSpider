# -*- coding: utf-8 -*-
import os
import re
import json
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
            'Host': 'torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

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
        proxies = random.choice(PROXIES)
        return proxies

    def r_first(self):
        r = self.session.get(self.url_code,headers=self.headers,proxies=self.proxies)
        print(r.status_code)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("{}/login/code/torum.png".format(path), 'wb').write(r.content)
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/code/torum.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1902)
        global err
        err = code["pic_id"]
        result = code ["pic_str"].lower()
        print(result)
        co = {
            'input':result,
            'submit':'Verify'
        }
        res = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=co)
        print(res.status_code)

    def r_second(self):
        resp = self.session.get(self.url2,headers=self.headers,proxies=self.proxies)
        print(resp.status_code)
        # print(resp.text)
        sid = re.findall(r'<dd><input type="hidden" name="sid" value="(.*?)" />', resp.text)[0]
        print(sid)
        creation_time = re.findall(r'<input type="hidden" name="creation_time" value="(.*?)" />', resp.text)[0]
        print(creation_time)
        form_token = re.findall(r'<input type="hidden" name="form_token" value="(.*?)" />', resp.text)[0]
        print(form_token)
        data = {
            'sid': sid,
            'creation_time':creation_time,
            'form_token':form_token,
            'username':'lantian',
            'password':'baiyun',
            'redirect':'./index.php?',
            'login':'Login',
        }
        return data

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)

    def r_third(self,data):
        response = self.session.post(self.url3,headers=self.headers,proxies=self.proxies,data=data)
        print(response.status_code)
        #print(response.text)
        if 'Beginners Lounge' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion' ".format(cookie_table)
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
        data = self.r_second()
        self.r_third(data)


if __name__ == '__main__':
    l = Login()
    l.main()