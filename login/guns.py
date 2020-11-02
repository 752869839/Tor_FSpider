# -*- coding: utf-8 -*-
import os
import json
import random
import requests
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import conn,table,cookie_table
from login.log_decorator import _logger, exception_logger

logger = _logger()

class GunsLogin(object):
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
            'Host': 'gunsganos2raowan5y2nkblujnmza32v2cwkdgy6okciskzabchx4iqd.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers


    def url(self):
        url = 'http://gunsganos2raowan5y2nkblujnmza32v2cwkdgy6okciskzabchx4iqd.onion/login.php'
        return url

    def url_code(self):
        url_code = 'http://gunsganos2raowan5y2nkblujnmza32v2cwkdgy6okciskzabchx4iqd.onion/securimage-master/securimage_show.php'
        return url_code

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
        logger.info('应用代理ip:')
        logger.info(proxies)
        return proxies

    def first(self):
        logger.info('开始登录!')
        r = self.session.get(self.url,headers=self.headers,proxies=self.proxies,timeout=30)
        logger.info('访问登录网址:')
        logger.info(r.status_code)
        res = self.session.get(self.url_code,headers=self.headers,proxies=self.proxies,timeout=30)
        logger.info('访问验证码链接:')
        logger.info(res.status_code)
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open( "{}/login/code/guns.png".format(path), 'wb').write(res.content)
        # open( "/code/tor_spider/img/guns.png", 'wb').write(res.content)
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im = open('{}/login/code/guns.png'.format(path), 'rb').read()
        # im = open('/code/tor_spider/img/guns.png', 'rb').read()
        code = chaojiying.PostPic(im, 1008)
        global err
        err = code["pic_id"]
        result = code ["pic_str"]
        logger.info('验证码识别结果为:')
        logger.info(result)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username,password FROM {} where domain='gunsganos2raowan5y2nkblujnmza32v2cwkdgy6okciskzabchx4iqd.onion'".format(cookie_table))
        acc = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        account = random.choice(acc)
        username = account[0]
        password = account[1]
        logger.info('获取登录用户名:')
        logger.info(username)
        logger.info('获取登录用户密码:')
        logger.info(password)
        data = {
            'captcha_code': result,
            'username': username,
            'password': password,
        }
        return data

    def error(self):
        chaojiying = Chaojiying_Client('chaojiyingcmq', 'cc123456', '868692')
        im_id = chaojiying.ReportError(err)
        print(im_id)

    def second(self,data):
        response = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=data,timeout=30)
        logger.info('请求提交登录表单:')
        logger.info(response.status_code)
        if 'Home' in response.text:
            logger.info('登录成功:')
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info('Cookie值:')
            logger.info(cookies)
            jsonCookies = json.dumps(cookies)
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='gunsganos2raowan5y2nkblujnmza32v2cwkdgy6okciskzabchx4iqd.onion' ".format(cookie_table)
            cursor.execute(sql, [jsonCookies])
            conn.commit()
            cursor.close()
            conn.close()
            logger.info('Cookie入库完毕,准备采集!')
            return jsonCookies
        else :
            self.error()
            self.main()

    @exception_logger(logger)
    def main(self):
        data = self.first()
        self.second(data)

if __name__ == '__main__':
    l = GunsLogin()
    l.main()