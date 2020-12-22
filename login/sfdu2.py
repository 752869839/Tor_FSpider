# -*- coding: utf-8 -*-
import os
import re
import json
import time
import random
import requests
from lxml import etree
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import SOCKS_PROXY,mysql_conn,table,cookie_table
from login.log_decorator import _logger, exception_logger

logger = _logger()
count = []
class Sfdu2Login(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.url = self.url()
        self.url1 = self.url1()
        self.url2 = self.url2()
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
            'Host': 'sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def url(self):
        url = 'http://sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion/protectd?invita='
        return url

    def url1(self):
        url1 = 'http://sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion/?invita='
        return url1

    def url2(self):
        url2 = 'http://sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion/site/loginp?invita='
        return url2


    def proxies(self):
        proxy = random.choice(SOCKS_PROXY).replace('socks5','socks5h')
        proxies = {"http":proxy}
        logger.info('应用代理ip为:')
        logger.info(proxies)
        return proxies

    def first(self):
        logger.info('开始登录:')
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        time.sleep(2)
        logger.info('访问登录网址:')
        logger.info(r.status_code)
        rs = self.session.get(self.url1,headers=self.headers,proxies=self.proxies)
        time.sleep(2)
        logger.info('访问第二层网址:')
        logger.info(rs.status_code)
        res = self.session.get(self.url2,headers=self.headers,proxies=self.proxies)
        time.sleep(3)
        logger.info('访问第三层网址:')
        logger.info(res.status_code)
        csrf = re.findall(r'name="_csrf-f".value="(.*?)">', res.text)[0]
        logger.info('获取csrf:')
        logger.info(csrf)
        html = etree.HTML(res.text)
        # captcha = re.findall(r'id="loginform-verifycode-image".src="(.*?)".alt',res.text)[0]
        captcha = html.xpath('//img[@id="loginform-verifycode-image"]/@src')[0]
        logger.info('获取captcha:')
        logger.info(captcha)
        url_code = 'http://sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion'+captcha
        resp = self.session.get(url_code,headers=self.headers,proxies=self.proxies)
        time.sleep(1)
        logger.info('访问验证码:')
        logger.info(resp.status_code)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # open( "{}/login/code/sfdu2.png".format(path), 'wb').write(resp.content)
        open( "/code/login/img/sfdu2.png", 'wb').write(resp.content)
        # im = open('{}/login/code/sfdu2.png'.format(path), 'rb').read()
        im = open('/code/login/img/sfdu2.png', 'rb').read()
        chaojiying = Chaojiying_Client()
        code = chaojiying.PostPic(im, 1006)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        logger.info('验证码识别结果为:')
        logger.info(result)
        mysql_conn.ping(reconnect=True)
        cursor = mysql_conn.cursor()
        cursor.execute(
            "SELECT username,password FROM {} where domain='sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion'".format(cookie_table))
        acc = cursor.fetchall()
        mysql_conn.commit()
        cursor.close()
        mysql_conn.close()
        account = random.choice(acc)
        username = account[0]
        password = account[1]
        logger.info('获取登录用户名:')
        logger.info(username)
        logger.info('获取登录用户密码:')
        logger.info(password)
        data = {
            '_csrf-f': csrf,
            'LoginForm[username]': username,
            'LoginForm[password]': password,
            'LoginForm[verifyCode]': result,
        }
        return data

    def error(self):
        chaojiying = Chaojiying_Client()
        im_id = chaojiying.ReportError(err)
        print(im_id)


    def second(self,data):
        response = self.session.post(self.url2,headers=self.headers,proxies=self.proxies,data=data)
        logger.info('请求提交登录表单:')
        logger.info(response.status_code)
        if '个人中心' in response.text:
            logger.info('登录成功!!!')
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info('Cookie值:')
            logger.info(cookies)
            jsonCookies = json.dumps(cookies)
            mysql_conn.ping(reconnect=True)
            cursor = mysql_conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            mysql_conn.commit()
            cursor.close()
            mysql_conn.close()
            logger.info('Cookie入库完毕,准备采集!')
            return jsonCookies
        else :
            if len(count) <= 3:
                self.error()
                return self.main()

    def main(self):
        count.append(1)
        data = self.first()
        self.second(data)


if __name__ == '__main__':
    l = Sfdu2Login()
    l.main()