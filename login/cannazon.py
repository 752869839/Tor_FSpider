# -*- coding: utf-8 -*-
import os
import json
import random
import requests
from lxml import etree
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import SOCKS_PROXY,mysql_conn,table,cookie_table
from login.mylog import logger


logger = logger()
count = []
class CannazonLogin(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.url = self.url()
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
            'Host': 'cannazondp5fciis.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers



    def url(self):
        url = 'http://cannazondp5fciis.onion/'
        return url


    def proxies(self):
        proxy = random.choice(SOCKS_PROXY).replace('socks5','socks5h')
        proxies = {"http":proxy}
        logger.info(f'应用代理ip为:{proxies}')
        return proxies

    def first(self):
        logger.info('开始登录:')
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info(f'访问登录网址,{r.status_code}')
        html = etree.HTML(r.text)
        code_url = html.xpath('//div[@class="col-md-6 col-md-offset-1 text-center"]/img/@src')[0]
        code_url = 'http://cannazondp5fciis.onion/' + code_url
        res = self.session.get(code_url,headers=self.headers,proxies=self.proxies)
        logger.info(f'访问验证码链接:{res.status_code}')
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open( "/code/login/img/cannazon.png", 'wb').write(res.content)
        im = open('/code/login/img/cannazon.png', 'rb').read()
        chaojiying = Chaojiying_Client()
        code = chaojiying.PostPic(im, 1008)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        logger.info(f'验证码识别结果为:{result}')
        data = {
            'captcha': result,
        }
        return data

    def second(self,data):
        response = self.session.post(self.url, headers=self.headers, proxies=self.proxies, data=data)
        logger.info(f'请求提交登录表单:{response.status_code}')
        if 'Welcome to Cannazon' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info(f'登录成功Cookie值:{cookies}')
            jsonCookies = json.dumps(cookies)
            mysql_conn.ping(reconnect=True)
            cursor = mysql_conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='cannazondp5fciis.onion' ".format(cookie_table)
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

    def error(self):
        chaojiying = Chaojiying_Client()
        im_id = chaojiying.ReportError(err)


    def main(self):
        count.append(1)
        data = self.first()
        self.second(data)


if __name__ == '__main__':
    l = CannazonLogin()
    l.main()