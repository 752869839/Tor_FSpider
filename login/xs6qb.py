# -*- coding: utf-8 -*-
import os
import json
import random
import requests
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import SOCKS_PROXY,mysql_conn,table,cookie_table
from login.mylog import logger

logger = logger()
count = []
class Xs6qbLogin(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.url = self.url()
        self.url2 = self.url2()
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
        "User-Agent":'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.5',
        'Host': 'xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests': '1' ,
        }
        return headers

    def url(self):
        url = 'http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion'
        return url

    def url2(self):
        url2 = 'http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion/entrance/logins.php'
        return url2

    def url_code(self):
        url_code = 'http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion/entrance/code76.php'
        return url_code

    def proxies(self):
        proxy = random.choice(SOCKS_PROXY).replace('socks5','socks5h')
        proxies = {"http":proxy}
        logger.info(f'应用代理ip为:{proxies}')
        return proxies

    def first(self):
        logger.info('开始登录:')
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info(f'访问登录网址,{r.status_code}')
        res = self.session.get(self.url_code,headers=self.headers,proxies=self.proxies)
        logger.info(f'访问验证码链接:{res.status_code}')
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open( "/code/login/img/xs6qb.png", 'wb').write(res.content)
        im = open('/code/login/img/xs6qb.png', 'rb').read()
        chaojiying = Chaojiying_Client()
        code = chaojiying.PostPic(im, 1006)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        logger.info(f'验证码识别结果为:{result}')
        mysql_conn.ping(reconnect=True)
        cursor = mysql_conn.cursor()
        cursor.execute(
            "SELECT username,password FROM {} where domain='xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion'".format(cookie_table))
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
            "lgid": username, "lgpass": password, "sub_code": result,
                      "lgsub": "lgsub"}
        return data


    def error(self):
        chaojiying = Chaojiying_Client()
        im_id = chaojiying.ReportError(err)

    def second(self,data):
        response = self.session.post(self.url2,headers=self.headers,proxies=self.proxies,data=data)
        logger.info(f'请求提交登录表单:{response.status_code}')
        if '账户中心' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info(f'登录成功Cookie值:{cookies}')
            jsonCookies = json.dumps(cookies)
            mysql_conn.ping(reconnect=True)
            cursor = mysql_conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion' ".format(cookie_table)
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
        form = self.first()
        self.second(form)


if __name__ == '__main__':
    l = Xs6qbLogin()
    l.main()