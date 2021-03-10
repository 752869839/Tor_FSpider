# -*- coding: utf-8 -*-
import os
import re
import json
import time
import random
import requests
import cairosvg
from lxml import etree
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import SOCKS_PROXY,mysql_conn,table,cookie_table
from login.mylog import logger

logger = logger()
count = []
class XbtppLogin(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.proxies = self.proxies()
        self.url = self.url()
        self.p_url = self.url_post()
        self.login_url = self.url_login()

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
            'Host': 'xbtppbb7oz5j2stohmxzvkprpqw5dwmhhhdo2ygv6c7cs4u46ysufjyd.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def url(self):
        url = 'http://2222222222vf2a2e.onion/'
        return url

    def url_post(self):
        p_url = 'http://xbtppbb7oz5j2stohmxzvkprpqw5dwmhhhdo2ygv6c7cs4u46ysufjyd.onion'
        return p_url

    def url_login(self):
        login_url = 'http://xbtppbb7oz5j2stohmxzvkprpqw5dwmhhhdo2ygv6c7cs4u46ysufjyd.onion/login'
        return login_url

    def proxies(self):
        proxy = random.choice(SOCKS_PROXY).replace('socks5','socks5h')
        proxies = {"http":proxy}
        logger.info(f'应用代理ip为:{proxies}')
        return proxies


    def first(self):
        r = self.session.get(self.p_url, headers=self.headers, proxies=self.proxies)
        logger.info(f'访问登录网址,{r.status_code}')
        time.sleep(3)
        res = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        logger.info(f'2访问登录网址,{res.status_code}')
        url_index = re.findall(r'url=(.*?)"> ', res.text)[0]
        logger.info(f'url_index:{url_index}')
        time.sleep(3)
        resp = self.session.get(url_index,headers=self.headers,proxies=self.proxies)
        time.sleep(3)
        logger.info(f'3访问登录网址,{resp.status_code}')
        response = etree.HTML(resp.text)
        svg = response.xpath('//p[@style="margin-bottom:20px"]/svg')[0]
        svg = etree.tostring(svg, encoding='utf-8')
        svg = str(svg, encoding='utf-8')
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open('/code/login/e43cg.svg','w',encoding='utf-8') as f1:
            f1.write(svg)
            f1.close()
        cairosvg.svg2png(file_obj=open('/code/login/e43cg.svg',"rb"), write_to='/code/login/e43cg.png')
        im = open('/code/login/e43cg.png', 'rb').read()
        chaojiying = Chaojiying_Client()
        code = chaojiying.PostPic(im, 1004)
        global err
        err = code["pic_id"]
        result = code["pic_str"].lower()
        logger.info(result)
        data = {"captcha":result}
        return data

    def second(self,data):
        res = self.session.post(url=self.p_url, headers=self.headers, proxies=self.proxies, data=data)
        logger.info(res.status_code)
        if '会员登录' in res.text:
            response = etree.HTML(res.text)
            svg = response.xpath('//div[@class="m-2"]/svg')[0]
            svg = etree.tostring(svg, encoding='utf-8')
            svg = str(svg, encoding='utf-8')
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            with open('/code/login/e43cg2.svg', 'w', encoding='utf-8') as f1:
                f1.write(svg)
                f1.close()
            cairosvg.svg2png(file_obj=open('/code/login/e43cg2.svg', "rb"),write_to='/code/login/e43cg2.png')
            im = open('/code/login/e43cg2.png', 'rb').read()
            chaojiying = Chaojiying_Client()
            code = chaojiying.PostPic(im, 1004)
            global err
            err = code["pic_id"]
            result = code["pic_str"].lower()
            logger.info(result)
            mysql_conn.ping(reconnect=True)
            cursor = mysql_conn.cursor()
            cursor.execute(
                "SELECT username,password FROM {} where domain='xbtppbb7oz5j2stohmxzvkprpqw5dwmhhhdo2ygv6c7cs4u46ysufjyd.onion'".format(
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
            form = {
                "name": username,
                "passwd": password,
                "captcha": result
            }
            return form

    def third(self,form):
        response = self.session.post(url=self.login_url, headers=self.headers, proxies=self.proxies, data=form)
        logger.info(f'请求提交登录表单:{response.status_code}')
        if '担保市场' in response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info(f'登录成功Cookie值:{cookies}')
            jsonCookies = json.dumps(cookies)
            mysql_conn.ping(reconnect=True)
            cursor = mysql_conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='xbtppbb7oz5j2stohmxzvkprpqw5dwmhhhdo2ygv6c7cs4u46ysufjyd.onion' ".format(
                cookie_table)
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
        logger.info(im_id)
        return im_id

    def main(self):
        count.append(1)
        data = self.first()
        form = self.second(data)
        self.third(form)


if __name__ == '__main__':
    l = XbtppLogin()
    l.main()