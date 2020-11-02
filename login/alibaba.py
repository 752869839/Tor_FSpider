# -*- coding: utf-8 -*-
import re
import os
import json
import random
import cairosvg
import requests
from lxml import etree
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import conn,table,cookie_table
from login.log_decorator import _logger, exception_logger

logger = _logger()

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
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT proxy FROM {} where project_name='tor_spider'".format(table))
        tor_proxy = json.loads(cursor.fetchone()[0])
        conn.commit()
        cursor.close()
        conn.close()
        proxy = random.choice(tor_proxy)
        proxies = {'http' : proxy}
        logger.info('应用代理ip为:')
        logger.info(proxies)
        return proxies


    def get(self):
        logger.info('开始登录:')
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info('访问登录网址:')
        logger.info(r.status_code)
        res = etree.HTML(r.text)
        captcha_url = res.xpath('//img[@style="float:right"]/@src')[0].strip().replace("'",'%27')
        logger.info('提取captcha_url:')
        logger.info(captcha_url)
        captcha_url = 'http://alibaba2kw6qoh6o.onion' + captcha_url
        resp = self.session.get(captcha_url,headers=self.headers,proxies=self.proxies)
        logger.info('访问验证码链接:')
        logger.info(resp.status_code)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open('{}/login/code/alibaba.svg'.format(path), 'w', encoding='utf-8') as f1:
        # with open('/code/tor_spider/img/alibaba.svg', 'w', encoding='utf-8') as f1:
            f1.write(resp.text)
            f1.close()

        cairosvg.svg2png(file_obj=open("{}/login/code/alibaba.svg".format(path), "rb"), write_to="{}/login/code/alibaba.png".format(path))
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/code/alibaba.png'.format(path), 'rb').read()
        # im = open('/code/tor_spider/img/alibaba.png', 'rb').read()
        code = chaojiying.PostPic(im, 1004)
        global err
        err = code["pic_id"]
        result = code ["pic_str"].lower()
        logger.info('验证码识别结果为:')
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
        print(im_id)

    def post(self,data):
        response = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=data)
        logger.info('请求提交验证码表单:')
        logger.info(response.status_code)
        if '会员登录' in response.text:
            captcha_url = re.findall('background: url(.*?) center',response.text)[0].replace("('",'').replace("'", '%27')
            logger.info('提取第二张验证码captcha_url:')
            logger.info(captcha_url)
            captcha_url = 'http://alibaba2kw6qoh6o.onion' + captcha_url
            resp = self.session.get(captcha_url, headers=self.headers, proxies=self.proxies)
            logger.info('请求验证码地址:')
            logger.info(response.status_code)
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            with open('{}/login/code/alibaba2.svg'.format(path), 'w', encoding='utf-8') as f1:
            # with open('/code/tor_spider/img/alibaba2.svg', 'w', encoding='utf-8') as f1:
                f1.write(resp.text)
                f1.close()
            cairosvg.svg2png(file_obj=open("{}/login/code/alibaba2.svg".format(path), "rb"),write_to="{}/login/code/alibaba2.png".format(path))
            chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
            im = open('{}/login/code/alibaba2.png'.format(path), 'rb').read()
            # im = open('/code/tor_spider/img/alibaba2.png', 'rb').read()
            code = chaojiying.PostPic(im, 1004)
            global err
            err = code["pic_id"]
            result = code["pic_str"].lower()
            logger.info('验证码识别结果为:')
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
            password = account[1]
            logger.info('获取登录用户名:')
            logger.info(username)
            logger.info('获取登录用户密码:')
            logger.info(password)
            form = {
                'captcha':result,
                'name':username,
                'passwd':password
            }
            return form
        else :
            self.error()
            self.main()

    def form_post(self,form):
        response = self.session.post(self.login_url,headers=self.headers,proxies=self.proxies,data=form)
        logger.info('请求提交登录表单:')
        logger.info(response.status_code)
        if 'Welcome to ' in response.text:
            logger.info('登录成功!!!')
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info('Cookie值:')
            logger.info(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql ="update {} SET cookie=%s  WHERE domain='alibaba2kw6qoh6o.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            conn.commit()
            cursor.close()
            conn.close()
            logger.info('Cookie入库完毕,准备采集!')
            return jsonCookies
        else:
            self.error()
            self.main()

    def main(self):
        data = self.get()
        form = self.post(data)
        self.form_post(form)

if __name__ == '__main__':
    l = AlibabaLogin()
    l.main()