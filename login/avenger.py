# -*- coding: utf-8 -*-
import re
import json
import random
import requests
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import conn,table,cookie_table
from login.log_decorator import _logger, exception_logger

logger = _logger()

class AvengerLogin(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.headers2 = self.headers2()
        self.url = self.url()
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
            'Host': 'avengersdutyk3xf.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def headers2(self):
        headers2 = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'avengersdutyk3xf.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'http://avengersdutyk3xf.onion/'
        }
        return headers2

    def url(self):
        url = 'http://avengersdutyk3xf.onion'
        return url

    def url2(self):
        url2 = 'http://avengersdutyk3xf.onion/member.php'
        return url2

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

    def first(self):
        logger.info('开始登录:')
        res = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info('访问登录网址:')
        logger.info(res.status_code)
        my_post_key = re.findall(r'<input name="my_post_key" type="hidden" value="(.*?)" />', res.text)[0]
        logger.info('提取my_post_key:')
        logger.info(res.my_post_key)
        data = {
            "action": "do_login", "url": "/index.php", "my_post_key": my_post_key,
                      "username": 'laoganma', "password": "Laoganma123", "remember": "yes"}
        return data

    def second(self,data):
        response = self.session.post(self.url2,headers=self.headers2,proxies=self.proxies,data=data)
        logger.info('请求提交登录表单:')
        logger.info(response.status_code)
        if 'Log Out' in response.text:
            logger.info('登录成功!!!')
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info('Cookie值:')
            logger.info(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='avengersdutyk3xf.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            conn.commit()
            cursor.close()
            conn.close()
            logger.info('Cookie入库完毕,准备采集!')
            return jsonCookies
        else :
            self.main()

    def main(self):
        data = self.first()
        self.second(data)

if __name__ == '__main__':
    l = AvengerLogin()
    l.main()