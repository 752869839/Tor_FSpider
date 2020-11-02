# -*- coding: utf-8 -*-
import os
import re
import base64
import random
import requests
from PIL import Image
from os import listdir
from requests_toolbelt import MultipartEncoder
from chaojiying import Chaojiying_Client
from config import PROXIES,conn,cookie_table

class Login(object):
    def __init__(self):
        self.session = self.r_session()
        self.headers = self.r_headers()
        self.proxies = self.r_proxies()
        self.url = self.r_url()
        self.p_url = self.r_url_post()

    def r_session(self):
        session = requests.session()
        return session

    def r_headers(self):
        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'danschat356lctri3zavzh6fbxg2a7lo6z3etgkctzzpspewu7zdsaqd.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def r_url(self):
        url = 'http://danschat356lctri3zavzh6fbxg2a7lo6z3etgkctzzpspewu7zdsaqd.onion/'
        return url

    def r_url_post(self):
        p_url = 'http://danschat356lctri3zavzh6fbxg2a7lo6z3etgkctzzpspewu7zdsaqd.onion/chat.php'
        return p_url

    def r_proxies(self):
        proxies = random.choice(PROXIES)
        return proxies

    def r_first(self):
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        print(r.status_code)
        url_code = re.findall('data:image/gif;base64,(.*?)">',r.text)[0]
        print(url_code)
        nc = re.findall('"nc" value="(.*?)">',r.text)[0]
        print(nc)
        challenge = re.findall('"challenge" value="(.*?)">',r.text)[0]
        print(challenge)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("{}/login/code/danschat.png".format(path), 'wb').write(base64.b64decode(url_code))

        im_list = [Image.open(fn) for fn in listdir() if fn.endswith('.png')]# 获取当前文件夹中所有JPG图像
        # 图片转化为相同的尺寸
        ims = []
        for i in im_list:
            new_img = i.resize((120, 70), Image.BILINEAR)
            ims.append(new_img)
        width, height = ims[0].size# 单幅图像尺寸
        result = Image.new(ims[0].mode, (width, height * len(ims)))# 创建空白长图
        # 拼接图片
        for i, im in enumerate(ims):
            result.paste(im, box=(0, i * height))
        # 保存图片
        result.save('{}/login/code/danschat.png'.format(path))

        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/code/danschat.png'.format(path), 'rb').read()
        code = chaojiying.PostPic(im, 6004)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        print(result)
        data = {
            'lang': 'en',
            'nc': nc,
            'action': 'login',
            'nick': 'nongfu',
            'pass': 'shanquan',
            'challenge': challenge,
            'captcha': result,
            'colour': '',
        }
        return data

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)
        return im_id


    def r_second(self,data):
        data = MultipartEncoder(fields=data)
        print(data)
        m_headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'danschat356lctri3zavzh6fbxg2a7lo6z3etgkctzzpspewu7zdsaqd.onion',
            'Cookie': 'language = en',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': data.content_type
        }
        response = self.session.post(self.p_url,headers=m_headers,proxies=self.proxies,data=data)
        print(response.status_code)
        #print(response.text)
        if 'http://www.w3.org/TR/html4/frameset.dtd' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            print(cookies)
            return cookies
        else :
            self.error()
            self.main()

    def main(self):
        data = self.r_first()
        self.r_second(data)

if __name__ == '__main__':
    l = Login()
    l.main()