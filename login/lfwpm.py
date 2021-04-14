# -*- coding: utf-8 -*-
import os
import re
import json
import time
import random
import requests
from urllib import parse
from lxml import etree
from login.chaojiying import Chaojiying_Client
from tor_spider.settings import proxy_table,cookie_table,mysql_conn,proxy_mysql_conn
from login.mylog import logger

logger = logger()
count = []
class LfwpmLogin(object):
    def __init__(self):
        self.session = self.session()
        self.headers = self.headers()
        self.headers1 = self.headers1()
        self.headers2 = self.headers2()
        self.url = self.url()
        self.url2 = self.url2()
        self.url3 = self.url3()
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
            'Content-Length':'87',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host': 'lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion',
            'Referer': 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        return headers

    def headers1(self):
        headers1 = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion',
            'Referer': 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/',
            'Connection': 'keep-alive',
        }
        return headers1

    def headers2(self):
        headers2 = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion',
            'Referer': 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/',
            'Connection': 'keep-alive',
            'X - Requested - With':'XMLHttpRequest'
        }
        return headers2

    def url(self):
        url = 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/'
        return url

    def url2(self):
        url2 = 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/misc.php?mod=seccode&action=update&idhash=cSA&0.3610130124744941&modid=member::logging'
        return url2

    def url3(self):
        url3 = 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
        return url3

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

    def suff(self):
        # res = self.session.get(self.url,headers=self.headers,proxies=self.proxies)
        mysql_conn.ping(reconnect=True)
        cursor = mysql_conn.cursor()
        cursor.execute(
            "SELECT username,password FROM {} where domain='lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion'".format(cookie_table))
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
            'fastloginfield': 'username',
            'username': 'nongfu',
            'password': 'shanquan',
            'quickforward': 'yes',
            'handlekey': 'ls'
        }
        resp = self.session.post(self.url3, headers=self.headers, proxies=self.proxies,data=data)
        logger.info(f'请求提交登录表单:{resp.status_code}')
        time.sleep(2)
        login_url = re.findall("'login',.'(.*?)referer=",resp.text)[0]
        logger.info(f'提取login_url:{login_url}')
        login_url = 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/{}referer=http%3A%2F%2Flfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion%2F&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'.format(login_url)
        login_url = parse.unquote(login_url)

        auth = re.findall("auth=(.*?)&referer",resp.text)[0]
        auth = parse.unquote(auth)
        logger.info(f'提取auth:{auth}')

        g_data = {
            'mod': 'logging',
            'action': 'login',
            'auth': auth,
            'referer': 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/',
            'infloat': 'yes',
            'handlekey': 'login',
            'inajax': '1',
            'ajaxtarget': 'fwin_content_login',
        }
        respon = self.session.post(login_url, headers=self.headers2, proxies=self.proxies, data=g_data)
        logger.info(f'提交表单请求:{respon.status_code}')
        time.sleep(2)
        response = self.session.get(self.url2, headers=self.headers1, proxies=self.proxies)
        logger.info(f'模拟ajax请求:{respon.status_code}')
        time.sleep(4)

        html = etree.HTML(response.text)
        url_code = html.xpath('//img[@class="vm"]/@src')[1]
        logger.info(f'提取url_code:{url_code}')
        url_code = 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/{}'.format(url_code)
        code_response = self.session.get(url_code, headers=self.headers2, proxies=self.proxies)
        logger.info(f'访问验证码链接:{code_response.status_code}')
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        open("/code/login/img/lfwpm.png", 'wb').write(code_response.content)
        im = open('/code/login/img/lfwpm.png', 'rb').read()
        chaojiying = Chaojiying_Client()
        code = chaojiying.PostPic(im, 1008)
        global err
        err = code["pic_id"]
        result = code["pic_str"].lower()
        logger.info(f'验证码识别结果为:{result}')
        post_code = 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/misc.php?mod=seccode&action=check&inajax=1&modid=member::logging&idhash=cSA&secverify={}'.format(result)

        code_data = {
            'mod': 'seccode',
            'action': 'check',
            'inajax': '1',
            'modid': 'member::logging',
            'idhash': 'cSA',
            'secverify': result,
        }
        formhash = re.findall('name="formhash" value="(.*?)" />',respon.text)[0]
        logger.info(f'提取formhash:{formhash}')

        loginhash = re.findall('loginhash=(.*?)">',respon.text)[0]
        logger.info(f'提取loginhash:{loginhash}')

        last_url = 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash={}&inajax=1'.format(loginhash)

        last_data = {
            'formhash': formhash,
            'referer': 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/',
            'auth': auth,
            'seccodehash': 'cSA',
            'seccodemodid': 'member::logging',
            'seccodeverify': result,
        }
        time.sleep(2)
        last_response = self.session.post(last_url, headers=self.headers, proxies=self.proxies,data=last_data)
        logger.info(f'模拟ajax请求:{last_response.status_code}')

        post_code_response = self.session.post(post_code, headers=self.headers2, proxies=self.proxies,data=code_data)
        logger.info(f'提交验证码表单请求:{post_code_response.status_code}')

        if '欢迎您回来' in last_response.text:
            cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
            logger.info(f'登录成功Cookie值:{cookies}')
            jsonCookies = json.dumps(cookies)
            mysql_conn.ping(reconnect=True)
            cursor = mysql_conn.cursor()
            sql = "update {} SET cookie=%s  WHERE domain='lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion' ".format(cookie_table)
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

    def error(self):
        chaojiying = Chaojiying_Client()
        im_id = chaojiying.ReportError(err)
        print(im_id)

    def main(self):
        count.append(1)
        jsonCookies =self.suff()
        return jsonCookies



if __name__ == '__main__':
    l = LfwpmLogin()
    l.main()


