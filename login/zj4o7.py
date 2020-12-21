# -*- coding: utf-8 -*-
import os
import re
import json
import time
import random
import requests
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import SOCKS_PROXY,mysql_conn,table,cookie_table
from login.log_decorator import _logger, exception_logger

logger = _logger()
count = []
class Zj4o7Login(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.url = self.url()
        self.url2 = self.url2()
        self.url3 = self.url3()
        self.url4 = self.url4()
        self.url_code = self.code()
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
            'Host': '7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def url(self):
        url = 'http://7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion/'
        return url

    def url2(self):
        url2 = 'http://7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion/user/login?tpl=def'
        return url2

    def url3(self):
        url3 = 'http://7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion/user/login'
        return url3

    def url4(self):
        url4 = 'http://7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion/user'
        return url4

    def code(self):
        url_code = 'http://7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion/other/vcode4'
        return url_code

    def proxies(self):
        proxy = random.choice(SOCKS_PROXY).replace('socks5','socks5h')
        proxies = {"http":proxy}
        logger.info('应用代理ip为:')
        logger.info(proxies)
        return proxies

    def first(self):
        logger.info('开始登录:')
        r = self.session.get(self.url2, headers=self.headers, proxies=self.proxies)
        time.sleep(1)
        logger.info('访问登录网址:')
        logger.info(r.status_code)
        res = self.session.get(self.url2,headers=self.headers,proxies=self.proxies)
        time.sleep(1)
        logger.info('访问登录链接:')
        logger.info(res.status_code)
        time.sleep(3)
        hash = re.findall(r'name="hash" value="(.*?)" />', res.text)[0]
        logger.info('配置登录需要hash值:')
        logger.info(hash)
        resp = self.session.get(self.url_code,headers=self.headers,proxies=self.proxies)
        time.sleep(1)
        logger.info('访问验证码链接:')
        logger.info(resp.status_code)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # open( "{}/login/code/zj4o7.png".format(path), 'wb').write(resp.content)
        open( "/code/login/img/zj4o7.png", 'wb').write(resp.content)
        # im = open('{}/login/code/zj4o7.png'.format(path), 'rb').read()
        im = open('/code/login/img/zj4o7.png', 'rb').read()
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
            "SELECT username,password FROM {} where domain='7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion'".format(cookie_table))
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
            'hash': hash,
            'username': username,
            'password': password,
            'vcode': result,
        }
        response = self.session.post(self.url3,headers=self.headers,proxies=self.proxies,data=data)
        logger.info('请求提交登录表单:')
        logger.info(response.status_code)
        return data

    def error(self):
        chaojiying = Chaojiying_Client()
        im_id = chaojiying.ReportError(err)
        print(im_id)


    def second(self,data):
        response = self.session.post(self.url4,headers=self.headers,proxies=self.proxies,data=data)
        logger.info('请求提交登录表单:')
        logger.info(response.status_code)
        if '退出' in response.text:
            logger.info('登录成功!!!')
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info('Cookie值:')
            logger.info(cookies)
            jsonCookies = json.dumps(cookies)
            mysql_conn.ping(reconnect=True)
            cursor = mysql_conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            mysql_conn.commit()
            cursor.close()
            mysql_conn.close()
            logger.info('Cookie入库完毕,开始采集!')
            return jsonCookies
        else :
            if len(count) <= 3:
                self.error()
                return self.main()

    @exception_logger(logger)
    def main(self):
        count.append(1)
        data = self.first()
        self.second(data)


if __name__ == '__main__':
    l = Zj4o7Login()
    l.main()