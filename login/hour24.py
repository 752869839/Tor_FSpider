# -*- coding: utf-8 -*-
import json
import random
import requests
from tor_spider.settings import proxy_table,cookie_table,mysql_conn,proxy_mysql_conn
from login.mylog import logger


logger = logger()

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
        proxy_mysql_conn.ping(reconnect=True)
        cursor = proxy_mysql_conn.cursor()
        cursor.execute(f"SELECT tunnelIP,tunnelPort FROM {proxy_table} where tunnelStatus=1")
        proxys = cursor.fetchall()
        proxy_list = []
        for proxy_tuple in proxys:
            proxy = f"socks5h://{proxy_tuple[0]}:{proxy_tuple[1]}"
            proxy_list.append(proxy)
        proxy_mysql_conn.commit()
        cursor.close()
        proxy_mysql_conn.close()
        proxy = random.choice(proxy_list)
        proxies = {"http":proxy}
        logger.info(f'应用代理ip为:{proxies}')
        return proxies

    def first(self):
        logger.info('开始登录:')
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info(f'访问登录网址,{r.status_code}')
        code = {
            'tor_key': '24SezAm'
        }
        response = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=code)
        logger.info(f'请求提交登录表单:{response.status_code}')
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        logger.info(f'登录成功Cookie值:{cookies}')
        jsonCookies = json.dumps(cookies)
        mysql_conn.ping(reconnect=True)
        cursor = mysql_conn.cursor()
        sql = "update {} SET cookie=%s  WHERE domain='24hourspkcmd7bvr.onion' ".format(cookie_table)
        cursor.execute(sql, [jsonCookies])
        mysql_conn.commit()
        cursor.close()
        mysql_conn.close()
        logger.info('Cookie入库完毕,准备采集!')
        return jsonCookies

    def main(self):
        self.first()


if __name__ == '__main__':
    l = Hour24Login()
    l.main()