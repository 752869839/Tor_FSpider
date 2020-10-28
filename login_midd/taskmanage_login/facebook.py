import json
import time
import pymysql
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login.connecting import conn
from login.config import table, cookie_table
from taskmanage.settings import logger


class Login(object):
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
        chromeOptions.add_argument('--headless')  # 谷歌无头模式
        chromeOptions.add_argument('--disable-gpu')  # 禁用显卡
        chromeOptions.add_argument('window-size=1280,800')  # 指定浏览器分辨率
        chromeOptions.add_argument("--no-sandbox")
        # chromeOptions.add_argument("--proxy-server=socks5://"+'45.77.172.182:8852')
        chromeOptions.add_argument("--proxy-server=" + self.proxie)  # 设置代理
        return chromeOptions

    def get_browser(self):
        browser = webdriver.Chrome(chrome_options=self.chromeOptions)
        return browser

    def get_wait(self):
        wait = WebDriverWait(self.browser, 10)
        return wait

    def login_url(self):
        try:
            self.browser.get(
                "https://www.facebookcorewwwi.onion/login/device-based/regular/login/?login_attempt=1&lwv=110")
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#loginbutton')))
            logger.info('The login page was accessed successfully')
        except:
            self.browser.refresh()
            time.sleep(10)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginbutton')))
            logger.info('The login page was accessed successfully')

    def login(self):
        try:
            conn.ping(reconnect=True)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username,password FROM {} where domain='facebookcorewwwi.onion'".format(cookie_table))
            acc = cursor.fetchall()
            conn.commit()
            cursor.close()
            conn.close()
            account = random.choice(acc)
            username = account[0]
            password = account[1]
            logger.info(username)
            logger.info(password)
            self.browser.find_element_by_xpath(
                '//*[@id="email"]').send_keys(username)
            self.browser.find_element_by_xpath(
                '//*[@id="pass"]').send_keys(password)
            self.browser.find_element_by_xpath('//*[@id="loginbutton"]').click()
            # self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#navItem_4748854339 > a:nth-child(2) > div:nth-child(2)')))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '._5qtp')))
            logger.info('login successfully')
            return username

        except:
            logger.info('Error correction')
            self.browser.refresh()
            time.sleep(5)
            self.main()

    def get_cookies(self, username):
        cookies = self.browser.get_cookies()
        jsonCookies = json.dumps(cookies)
        return username, jsonCookies
        # conn = pymysql.connect(host=host, user=user, password=password, database=database)  # 连接mysql数据库
        # cursor = conn.cursor()  # 创建游标对象
        # sql = "insert into facebook(cookies) values (%s);"
        # logger.info(jsonCookies)
        # cookies = jsonCookies
        # cursor.execute(sql, cookies)
        # conn.commit()  # 提交
        # cursor.close()
        # conn.close()

    def main(self):
        try:
            self.login_url()
            username = self.login()
            username, jsonCookies = self.get_cookies(username)
            self.browser.quit()
            return username, jsonCookies
        except:
            self.browser.quit()


if __name__ == '__main__':
    testspider = Login()
    testspider.main()
