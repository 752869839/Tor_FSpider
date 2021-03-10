# -*- coding: utf-8 -*-
import re
import os
import json
import random
import cairosvg
import requests
from lxml import etree
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import SOCKS_PROXY,mysql_conn,table,cookie_table
from login.mylog import logger

logger = logger()
count = []
class AlibabaLogin(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.url = self.url()
        self.login_url = self.login_url()
        self.proxies = self.proxies()

    def session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        logger.info('任务获取成功,准备登录')
        return session

    def headers(self):
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


    def url(self):
        url = 'http://alibaba2kw6qoh6o.onion/'
        return url

    def login_url(self):
        login_url = 'http://alibaba2kw6qoh6o.onion/login'
        return login_url

    def proxies(self):
        proxy = random.choice(SOCKS_PROXY).replace('socks5','socks5h')
        proxies = {"http":proxy}
        logger.info(f'应用代理ip为:{proxies}')
        return proxies


    def get(self):
        logger.info('开始登录:')
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info(f'访问登录网址,{r.status_code}')
        html = etree.HTML(r.text)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        captcha = html.xpath('//div[@style="float:right"]/svg')[0]
        with open('/code/login/img/alibaba.svg', 'wb') as f1:
            f1.write(etree.tostring(captcha))
            f1.close()
        cairosvg.svg2png(file_obj=open("/code/login/img/alibaba.svg", "rb"), write_to="/code/login/img/alibaba.png")
        im = open('/code/login/img/alibaba.png', 'rb').read()
        chaojiying = Chaojiying_Client()
        code = chaojiying.PostPic(im, 1004)
        global err
        err = code["pic_id"]
        result = code ["pic_str"].lower()
        logger.info(f'验证码识别结果为:{result}')
        # if len(result) < 4:
        #     self.main()
        data = {
            'captcha': result,
        }
        return data

    def error(self):
        chaojiying = Chaojiying_Client()
        im_id = chaojiying.ReportError(err)
        print(im_id)

    def post(self,data):
        response = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=data)
        logger.info('请求提交验证码表单:')
        logger.info(response.status_code)
        if '会员登录' in response.text:
            html2 = etree.HTML(response.text)
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            captcha = html2.xpath('//div[@class="flex-end"]/label/svg')[0]
            with open('/code/login/img/alibaba2.svg', 'wb') as f1:
                f1.write(etree.tostring(captcha))
                f1.close()
            cairosvg.svg2png(file_obj=open("/code/login/img/alibaba2.svg", "rb"),write_to="/code/login/img/alibaba2.png")
            im = open('/code/login/img/alibaba2.png', 'rb').read()
            chaojiying = Chaojiying_Client()
            code = chaojiying.PostPic(im, 1004)
            global err
            err = code["pic_id"]
            result = code["pic_str"].lower()
            logger.info(f'验证码识别结果为:{result}')
            mysql_conn.ping(reconnect=True)
            cursor = mysql_conn.cursor()
            cursor.execute(
                "SELECT username,password FROM {} where domain='alibaba2kw6qoh6o.onion'".format(cookie_table))
            acc = cursor.fetchall()
            mysql_conn.commit()
            cursor.close()
            mysql_conn.close()
            account = random.choice(acc)
            username = account[0]
            password = account[1]
            logger.info(f'登录用户名:{username}')
            logger.info(f'登录用户密码:{password}')
            form = {
                'captcha':result,
                'name':username,
                'passwd':password
            }
            return form
        else :
            if len(count) <= 3:
                self.error()
                return self.main()

    def form_post(self,form):
        response = self.session.post(self.login_url,headers=self.headers,proxies=self.proxies,data=form)
        logger.info(f'请求提交登录表单:{response.status_code}')
        if 'Welcome to ' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info(f'登录成功Cookie值:{cookies}')
            jsonCookies = json.dumps(cookies)
            mysql_conn.ping(reconnect=True)
            cursor = mysql_conn.cursor()
            sql ="update {} SET cookie=%s  WHERE domain='alibaba2kw6qoh6o.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            mysql_conn.commit()
            cursor.close()
            mysql_conn.close()
            logger.info('Cookie入库完毕,准备采集!')
            return jsonCookies
        else:
            if len(count) <= 3:
                self.error()
                return self.main()

    def main(self):
        count.append(1)
        data = self.get()
        form = self.post(data)
        self.form_post(form)

if __name__ == '__main__':
    l = AlibabaLogin()
    l.main()