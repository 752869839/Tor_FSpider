# -*- coding: utf-8 -*-
import os
import re
import json
import time
import base64
import random
import requests
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import proxy_table,cookie_table,mysql_conn,proxy_mysql_conn
from login.mylog import logger

logger = logger()
count = []
class PncldLogin(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.url = self.url()
        self.url2 = self.url2()
        self.url_verify = self.verify()
        self.proxies = self.proxies()

    def session(self):
        session = requests.session()
        session.keep_alive = False
        session.adapters.DEFAULT_RETRIES = 10
        logger.info('任务获取成功,准备登录')
        return session

    def headers(self):
        headers = {
            'Host': 'pncldyerk4gqofhp.onion',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        return headers

    def url(self):
        url = 'http://pncldyerk4gqofhp.onion/'
        return url

    def url2(self):
        url2 = "http://pncldyerk4gqofhp.onion/free/member.php"
        return url2

    def verify(self):
        url_verify = 'http://pncldyerk4gqofhp.onion/verify'
        return url_verify

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
        r = self.session.get(self.url, headers=self.headers, proxies=self.proxies)
        logger.info(f'访问登录网址,{r.status_code}')
        time.sleep(3)
        res = self.session.get(self.url, headers=self.headers, proxies=self.proxies)
        logger.info(f'再次访问登录网址,{res.status_code}')

        url_code = re.findall(r'<img src="data:image/gif;base64,(.*?)" width="150"', res.text)[0]
        logger.info(f'获取验证码的base64码:{url_code}')

        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("/code/login/img/pncld.png", 'wb').write(base64.b64decode(url_code))
        im = open('/code/login/img/pncld.png', 'rb').read()
        chaojiying = Chaojiying_Client()
        code = chaojiying.PostPic(im, 1006)
        global err
        err = code["pic_id"]
        result = code["pic_str"]
        results = result.lower()
        logger.info(f'验证码识别结果为:{result}')
        challenge = re.findall(r'name="challenge" value="(.*?)"><', res.text)[0]
        logger.info(f'获取challenge:{challenge}')
        form = {
            'captcha': results,
            'challenge': challenge,
            'location': 'A',
            'action': 'do_cap',
            'url': '/403.html'
        }
        return form

    def second(self,form):
        try:
            resp = self.session.post(self.url_verify, headers=self.headers, data=form, proxies=self.proxies)
            logger.info(f'提交验证码表单:{resp.status_code}')
            my_post_key = re.findall(r'"my_post_key" type="hidden" value="(.*?)" /> <table', resp.text)[0]
            logger.info(f'获取my_post_key:{my_post_key}')
            mysql_conn.ping(reconnect=True)
            cursor = mysql_conn.cursor()
            cursor.execute(
                "SELECT username,password FROM {} where domain='pncldyerk4gqofhp.onion'".format(
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
                'action': 'do_login',
                'url': "/free/index.php",
                'my_post_key': my_post_key,
                'username': username,
                'password': password,
            }
            return data
        except:
            self.main()

    def third(self,data):
        resp = self.session.post(self.url2, headers=self.headers, data=data, proxies=self.proxies)
        logger.info(f'请求提交登录表单:{resp.status_code}')
        response = self.session.get(self.url2, headers=self.headers, proxies=self.proxies)
        logger.info(f'请求主页地址:{response.status_code}')
        if '歡迎您回來' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info(f'登录成功Cookie值:{cookies}')
            jsonCookies = json.dumps(cookies)
            mysql_conn.ping(reconnect=True)
            cursor = mysql_conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='pncldyerk4gqofhp.onion' ".format(cookie_table)
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
        form = self.first()
        data = self.second(form)
        self.third(data)


if __name__ == '__main__':
    l = PncldLogin()
    l.main()