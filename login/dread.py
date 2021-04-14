# -*- coding: utf-8 -*-
import re
import time
import json
import random
import requests
from chaojiying import Chaojiying_Client
from login.mylog import logger

logger = logger()
count = []
class DreadLogin(object):
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
            'Host': 'dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def url(self):
        url = 'http://dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxknyazubrad.onion/'
        return url


    def proxies(self):
        proxies = {"http":'socks5h://172.16.20.125:1234'}
        logger.info(f'应用代理ip为:{proxies}')
        return proxies

    def first(self):
        self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        time.sleep(10)
        res = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info(f'访问登录网址,{res.status_code}')
        logger.info(res.text)
        code_img =  re.findall('background-image:url\((.*?)"></div>',res.text)[1]
        logger.info(code_img)


    def main(self):
        count.append(1)
        data = self.first()


if __name__ == '__main__':
    l = DreadLogin()
    l.main()
