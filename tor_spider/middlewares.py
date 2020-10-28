# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import time
import random
import scrapy
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from tor_spider.settings import table,cookie_table,conn
from scrapy.utils.project import get_project_settings

#IPMiddleware
# class IpProxyDownloadMiddleware(object):
#     def process_request(self, request, spider):
#         settings = get_project_settings()
#         proxy = random.choice(settings.get('HTTP_PROXY'))
#         request.meta['proxy'] = proxy

class SocksProxyDownloadMiddleware(object):
    def process_request(self, request, spider):
        settings = get_project_settings()
        request.meta['proxy'] = random.choice(settings.get('SOCKS_PROXY'))

class IpProxyDownloadMiddleware(object):
    conn.ping(reconnect=True)
    cursor = conn.cursor()
    cursor.execute("SELECT proxy FROM {} where project_name='Agarth'".format(table))
    PROXIES = json.loads(cursor.fetchone()[0])
    conn.commit()
    cursor.close()
    conn.close()

    def process_request(self, request, spider):
        proxy = random.choice(self.PROXIES)
        request.meta['proxy'] = proxy


#CookieMiddleware
class Agarth_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        #cursor.execute("SELECT cookies FROM agarth order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='agarthaangodtcz3.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]     # fetchall是在两个嵌套元组里fetchone在一个元组里
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None


class Alibaba_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        #cursor.execute("SELECT cookies FROM alibaba order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='alibaba2kw6qoh6o.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None

    def process_response(self, request, response, spider):
        if response.status == 302  :
            request.cookies = self.get_cookie_mysql()
            return request
        else:
            return response


class Apollo_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        #cursor.execute("SELECT cookies FROM apollo order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='apollonvm7uin7yw.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None

    def process_response(self, request, response, spider):
        if response.status == 302 :
            request.cookies = self.get_cookie_mysql()
            return request
        else:
            return response


class Avenger_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        #cursor.execute("SELECT cookies FROM avenger order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='avengersdutyk3xf.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None

    # def process_response(self, request, response, spider):
    #     if response.status == 403 :
    #         request.cookies = self.get_cookie_mysql()
    #         return request
    #     else:
    #         return response


class C2p3h_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        #cursor.execute("SELECT cookies FROM c2p3h order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None


class Cryptbbs_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        #cursor.execute("SELECT cookies FROM cryptbbs order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='cryptbb2gezhohku.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None


class Facebook_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        # cursor.execute("SELECT cookies FROM facebook order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='facebookcorewwwi.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None



class Facebook_SeleniumMiddleware(object):
    def __init__(self):
        self.proxie = self.r_proxies()
        self.chromeOptions = self.get_chrome()
        self.browser = self.get_browser()
        self.wait = self.get_wait()


    def r_proxies(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        cursor.execute("SELECT proxy FROM {} where project_name='Facebook'".format(table))
        PROXIES = json.loads(cursor.fetchone()[0])
        conn.commit()
        cursor.close()
        conn.close()
        proxie = random.choice(PROXIES)
        return proxie

    def get_chrome(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')             # 谷歌无头模式
        chromeOptions.add_argument('--disable-gpu')          # 谷歌文档提到需要加上这个属性来规避bug 这是禁用显卡
        chromeOptions.add_argument('window-size=1280,800')  # 指定浏览器分辨率
        chromeOptions.add_argument("--no-sandbox")
        # chromeOptions.add_argument("--proxy-server=socks5://"+'45.77.172.182:8852')
        chromeOptions.add_argument("--proxy-server="+self.proxie)        # 设置代理
        return chromeOptions

    def get_browser(self):
        browser = webdriver.Chrome(chrome_options=self.chromeOptions)
        #browser.set_window_size(1280,800)
        return browser

    def get_wait(self):
        wait = WebDriverWait(self.browser, 10)     # 强制等待10s
        return wait

    def process_request(self, request, spider):
        try:
            if request.url != 'http://avengersdutyk3xf.onion':
                conn.ping(reconnect=True)
                cursor = conn.cursor()
                # cursor.execute("SELECT cookies FROM facebook order by id desc limit 0,1")
                cursor.execute("SELECT cookie FROM {} where domain='facebookcorewwwi.onion' order by gmt_modified desc".format(cookie_table))
                cookies = cursor.fetchone()[0]
                conn.commit()
                cursor.close()
                conn.close()
                listcookies = json.loads(cookies)
                #self.browser.delete_all_cookies()
                print('request.url:',request.url)
                self.browser.get(request.url)
                for item in listcookies:
                    # print('item:',item)
                    self.browser.add_cookie(item)
                self.browser.get(request.url)
                for i in range(10):
                    self.browser.execute_script(
                        "var q=document.documentElement.scrollTop={}".format(i * 3000))  # 执行js语句,模拟下滑
                    time.sleep(0.5)
                # 执行js语句滑到最底部
                self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                html = self.browser.page_source
                self.browser.quit()
                return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',
                                                request=request)
        except:
            self.browser.quit()

class Guns_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        #cursor.execute("SELECT cookies FROM hour24 order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='gunsganos2raowan5y2nkblujnmza32v2cwkdgy6okciskzabchx4iqd.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None

class Gw6zz_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        #cursor.execute("SELECT cookies FROM hour24 order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='gw6zzvqgy6v2czxrmphuerrtbirftvkyfkeoaiorg5qijqlsbqfpqjqd.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None


class Hour24_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        #cursor.execute("SELECT cookies FROM hour24 order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='24hourspkcmd7bvr.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None

    def process_response(self, request, response, spider):
        if response.status == 403  :
            request.cookies = self.get_cookie_mysql()
            return request
        else:
            return response


class Lfwpm_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        #cursor.execute("SELECT cookies FROM lfwpm order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None

class Pncld_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        #cursor.execute("SELECT cookies FROM pncld order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='pncldyerk4gqofhp.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None


class Sfdu2_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()  # 创建游标对象
        #cursor.execute("SELECT cookies FROM sfdu2 order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None

    def process_response(self, request, response, spider):
        if request.url == 'http://sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion/protectd?invita='  :
            request.cookies = self.get_cookie_mysql()
            return request
        else:
            return response

class Torum_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        #cursor.execute("SELECT cookies FROM torum order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None

    def process_response(self, request, response, spider):
        if response.status == 302 :
            request.cookies = self.get_cookie_mysql()
            return request
        else:
            return response

class Xbtpp_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        # cursor.execute("SELECT cookies FROM xbtpp order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='xbtppbb7oz5j2stohmxzvkprpqw5dwmhhhdo2ygv6c7cs4u46ysufjyd.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None


class Xs6qb_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        #cursor.execute("SELECT cookies FROM xs6qb order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None


class Zj4o7_CookieMiddleware(RetryMiddleware):
    def __init__(self, settings, crawler):
        RetryMiddleware.__init__(self, settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)

    def get_cookie_mysql(self):
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        # cursor.execute("SELECT cookies FROM zj4o7 order by id desc limit 0,1")
        cursor.execute("SELECT cookie FROM {} where domain='7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion' order by gmt_modified desc".format(cookie_table))
        cookies = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        listcookies = json.loads(cookies)
        return listcookies

    def process_request(self, request, spider):
        request.cookies = self.get_cookie_mysql()
        return None


