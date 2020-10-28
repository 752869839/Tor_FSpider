# -*- coding: utf-8 -*-
import os
import re
import json
import time
import random
import requests
import cairosvg
from lxml import etree
from chaojiying import Chaojiying_Client
from config import PROXIES,conn,cookie_table

class Login(object):
    def __init__(self):
        self.session = self.r_session()
        self.headers = self.r_headers()
        self.proxies = self.r_proxies()
        self.url = self.r_url()
        self.p_url = self.r_url_post()
        self.login_url = self.r_url_login()

    def r_session(self):
        session = requests.session()
        return session

    def r_headers(self):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'xbtppbb7oz5j2stohmxzvkprpqw5dwmhhhdo2ygv6c7cs4u46ysufjyd.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def r_url(self):
        url = 'http://2222222222vf2a2e.onion/'
        return url

    def r_url_post(self):
        p_url = 'http://xbtppbb7oz5j2stohmxzvkprpqw5dwmhhhdo2ygv6c7cs4u46ysufjyd.onion'
        return p_url

    def r_url_login(self):
        login_url = 'http://xbtppbb7oz5j2stohmxzvkprpqw5dwmhhhdo2ygv6c7cs4u46ysufjyd.onion/login'
        return login_url

    def r_proxies(self):
        proxies = random.choice(PROXIES)
        return proxies

    def r_first(self):
        r = self.session.get(self.p_url, headers=self.headers, proxies=self.proxies)
        print(r.status_code)
        time.sleep(3)
        res = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        print(res.status_code)
        #print(r.text)
        url_index = re.findall(r'url=(.*?)"> ', res.text)[0]
        print(url_index)
        time.sleep(3)
        resp = self.session.get(url_index,headers=self.headers,proxies=self.proxies)
        time.sleep(3)
        print(resp.status_code)
        #print(resp.text)
        response = etree.HTML(resp.text)
        svg = response.xpath('//p[@style="margin-bottom:20px"]/svg')[0]
        svg = etree.tostring(svg, encoding='utf-8')
        svg = str(svg, encoding='utf-8')
        #print(svg)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open('{}/login/code/e43cg.svg'.format(path),'w',encoding='utf-8') as f1:
            f1.write(svg)
            f1.close()
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # url_path = os.path.join(path, "login", "e43cg.svg")
        # write_path = os.path.join(path, "login", "e43cg.png")
        # cairosvg.svg2png(file_obj=open(url_path, "rb"), write_to=write_path)
        cairosvg.svg2png(file_obj=open('{}/login/code/e43cg.svg'.format(path),"rb"), write_to='{}/login/code/e43cg.png'.format(path))

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)
        return im_id

    def r_second(self):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/code/e43cg.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1004)
        global err
        err = code["pic_id"]
        result = code["pic_str"].lower()
        print(result)
        data = {"captcha":result}
        return data

    def r_third(self,data):
        res = self.session.post(url=self.p_url,headers=self.headers,proxies=self.proxies,data=data)
        print(res.status_code)
        #print(res.text)
        if '会员登录' in res.text:
            response = etree.HTML(res.text)
            svg = response.xpath('//div[@class="m-2"]/svg')[0]
            svg = etree.tostring(svg, encoding='utf-8')
            svg = str(svg, encoding='utf-8')
            #print(svg)
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            with open('{}/login/code/e43cg2.svg'.format(path), 'w', encoding='utf-8') as f1:
                f1.write(svg)
                f1.close()
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # url_path = os.path.join(path, "login", "e43cg2.svg")
            # write_path = os.path.join(path, "login", "e43cg2.png")
            #cairosvg.svg2png(file_obj=open('e43cg2.svg', "rb"), write_to='e43cg2.png')
            cairosvg.svg2png(file_obj=open('{}/login/code/e43cg2.svg'.format(path), "rb"),write_to='{}/login/code/e43cg2.png'.format(path))
        else:
            self.main()

    def r_fourth(self):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/code/e43cg2.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 1004)
        global err
        err = code["pic_id"]
        result = code["pic_str"].lower()
        print(result)
        form = {
            "name": "q377877",
            "passwd" : "377877",
            "captcha": result
        }
        return form

    def r_fifth(self,form):
        response = self.session.post(url=self.login_url,headers=self.headers,proxies=self.proxies,data=form)
        print(response.status_code)
        if '担保市场' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='xbtppbb7oz5j2stohmxzvkprpqw5dwmhhhdo2ygv6c7cs4u46ysufjyd.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            conn.commit()
            cursor.close()
            conn.close()
            return jsonCookies
        else:
            self.main()

    def main(self):
        self.r_first()
        data = self.r_second()
        self.r_third(data)
        form = self.r_fourth()
        self.r_fifth(form)

if __name__ == '__main__':
    l = Login()
    l.main()