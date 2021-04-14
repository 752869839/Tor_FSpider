# -*- coding: utf-8 -*-
import os
import json
import random
import requests
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import proxy_table,cookie_table,mysql_conn,proxy_mysql_conn
from login.mylog import logger

logger = logger()
count = []
class C2p3hLogin(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.url = self.url()
        self.url_code = self.url_code()
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
            'Host': 'c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers


    def url(self):
        url = 'http://c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion/login'
        return url

    def url_code(self):
        url_code = 'http://c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion/jcaptcha.jpg'
        return url_code

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

    def get(self):
        logger.info('开始登录:')
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info(f'访问登录网址,{r.status_code}')
        logger.info(r.status_code)
        res = self.session.get(self.url_code,headers=self.headers,proxies=self.proxies)
        logger.info(f'访问验证码网址,{res.status_code}')
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open( "/code/login/img/c2p3h.png", 'wb').write(res.content)
        im = open('/code/login/img/c2p3h.png', 'rb').read()
        chaojiying = Chaojiying_Client()
        code = chaojiying.PostPic(im, 1008)
        global err
        err = code["pic_id"]
        result = code ["pic_str"].lower()
        logger.info(f'验证码识别结果为:{result}')
        mysql_conn.ping(reconnect=True)
        cursor = mysql_conn.cursor()
        cursor.execute(
            "SELECT username,password FROM {} where domain='c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion'".format(
                cookie_table))
        acc = cursor.fetchall()
        mysql_conn.commit()
        cursor.close()
        mysql_conn.close()
        account = random.choice(acc)
        username = account[0]
        password = account[1]
        logger.info(f'登录用户名:{username}')
        logger.info(f'登录用户密码:{password}')
        data = {
            'captcha': result,
            'username': username,
            'password': password,
        }
        return data

    def error(self):
        chaojiying = Chaojiying_Client()
        im_id = chaojiying.ReportError(err)
        print(im_id)

    def post(self,data):
        response = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=data)
        logger.info(f'请求提交登录表单:{response.status_code}')
        if '您当前为：非 VIP' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info(f'登录成功Cookie值:{cookies}')
            jsonCookies = json.dumps(cookies)
            mysql_conn.ping(reconnect=True)
            cursor = mysql_conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion' ".format(cookie_table)
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
        data = self.get()
        self.post(data)

if __name__ == '__main__':
    l = C2p3hLogin()
    l.main()