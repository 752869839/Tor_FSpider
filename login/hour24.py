# -*- coding: utf-8 -*-
import json
import random
import requests
from tor_spider.settings import conn,table,cookie_table
from login.log_decorator import _logger, exception_logger

logger = _logger()

class Hour24Login(object):
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
            'Host': '24hourspkcmd7bvr.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def url(self):
        url = 'http://24hourspkcmd7bvr.onion/'
        return url

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
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info('访问登录网址:')
        logger.info(r.status_code)
        code = {
            'tor_key': '24SezAm'
        }
        response = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=code)
        logger.info('请求提交登录表单:')
        logger.info(response.status_code)
        logger.info('登录成功!!!')
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        logger.info('Cookie值:')
        logger.info(cookies)
        jsonCookies = json.dumps(cookies)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        sql = "update {} SET cookie=%s  WHERE domain='24hourspkcmd7bvr.onion' ".format(cookie_table)
        cursor.execute(sql, [jsonCookies])
        conn.commit()
        cursor.close()
        conn.close()
        logger.info('Cookie入库完毕,准备采集!')
        return jsonCookies

    def main(self):
        self.first()


if __name__ == '__main__':
    l = Hour24Login()
    l.main()