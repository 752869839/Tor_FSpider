# -*- coding: utf-8 -*-
import os
import re
import json
import random
import requests
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import SOCKS_PROXY,mysql_conn,table,cookie_table
from login.mylog import logger

logger = logger()
count = []
class TorumLogin(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.url = self.url()
        self.url2 = self.url2()
        self.url3 = self.url3()
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
            'Host': 'torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def url(self):
        url = 'http://torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion/captcha/'
        return url

    def url2(self):
        url2 = 'http://torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion/'
        return url2

    def url3(self):
        url3 = 'http://torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion/ucp.php?mode=login'
        return url3

    def url_code(self):
        url_code = 'http://torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion/captcha/image.php'
        return url_code

    def proxies(self):
        proxy = random.choice(SOCKS_PROXY).replace('socks5','socks5h')
        proxies = {"http":proxy}
        logger.info(f'应用代理ip为:{proxies}')
        return proxies

    def first(self):
        logger.info('开始登录:')
        r = self.session.get(self.url_code,headers=self.headers,proxies=self.proxies)
        logger.info(f'访问验证码,{r.status_code}')
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("/code/login/img/torum.png", 'wb').write(r.content)
        im = open('/code/login/img/torum.png', 'rb').read()
        chaojiying = Chaojiying_Client()
        code = chaojiying.PostPic(im, 1902)
        global err
        err = code["pic_id"]
        result = code ["pic_str"].lower()
        logger.info(f'验证码识别结果为:{result}')
        co = {
            'input':result,
            'submit':'Verify'
        }
        res = self.session.post(self.url,headers=self.headers,proxies=self.proxies,data=co)
        logger.info(f'提交验证码表单:{res.status_code}')

    def second(self):
        resp = self.session.get(self.url2,headers=self.headers,proxies=self.proxies)
        logger.info(f'请求登录地址:{resp.status_code}')
        sid = re.findall(r'<dd><input type="hidden" name="sid" value="(.*?)" />', resp.text)[0]
        logger.info(f'提取sid:{sid}')
        creation_time = re.findall(r'<input type="hidden" name="creation_time" value="(.*?)" />', resp.text)[0]
        logger.info(f'提取creation_time:{creation_time}')
        form_token = re.findall(r'<input type="hidden" name="form_token" value="(.*?)" />', resp.text)[0]
        logger.info(f'提取form_token:{form_token}')
        mysql_conn.ping(reconnect=True)
        cursor = mysql_conn.cursor()
        cursor.execute(
            "SELECT username,password FROM {} where domain='torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion'".format(cookie_table))
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
            'sid': sid,
            'creation_time':creation_time,
            'form_token':form_token,
            'username':username,
            'password':password,
            'redirect':'./index.php?',
            'login':'Login',
        }
        return data

    def error(self):
        chaojiying = Chaojiying_Client()
        im_id = chaojiying.ReportError(err)

    def third(self,data):
        response = self.session.post(self.url3,headers=self.headers,proxies=self.proxies,data=data)
        logger.info(f'请求提交登录表单:{response.status_code}')
        if 'Beginners Lounge' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info(f'登录成功Cookie值:{cookies}')
            jsonCookies = json.dumps(cookies)
            mysql_conn.ping(reconnect=True)
            cursor = mysql_conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion' ".format(cookie_table)
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
        self.first()
        data = self.second()
        self.third(data)


if __name__ == '__main__':
    l = TorumLogin()
    l.main()