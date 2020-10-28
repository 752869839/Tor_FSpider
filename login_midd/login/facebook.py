import json
import time
import pymysql
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import PROXIES,conn,cookie_table

class Login(object):
    def __init__(self):
        self.proxie = self.r_proxies()
        self.chromeOptions = self.get_chrome()
        self.browser = self.get_browser()
        self.wait = self.get_wait()


    def r_proxies(self):
        proxie = random.choice(PROXIES)
        print(proxie)
        return proxie

    def get_chrome(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--headless')             # 谷歌无头模式
        chromeOptions.add_argument('--disable-gpu')          # 禁用显卡
        chromeOptions.add_argument('window-size=1280,800')  # 指定浏览器分辨率
        chromeOptions.add_argument("--no-sandbox")
        # chromeOptions.add_argument("--proxy-server=socks5://"+'45.77.172.182:8852')
        chromeOptions.add_argument("--proxy-server="+self.proxie)        # 设置代理
        return chromeOptions

    def get_browser(self):
        browser = webdriver.Chrome(chrome_options=self.chromeOptions)
        return browser

    def get_wait(self):
        wait = WebDriverWait(self.browser, 10)
        return wait

    def login_url(self):
        try:
            self.browser.get("https://www.facebookcorewwwi.onion/login/device-based/regular/login/?login_attempt=1&lwv=110")
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '._50f6')))
            time.sleep(3)
            print('The login page was accessed successfully')
        except:
            self.browser.refresh()
            time.sleep(3)
            self.login_url()
            print('The login page was accessed successfully')

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
            print(username)
            print(password)
            self.browser.find_element_by_xpath(
                '//*[@id="email"]').send_keys(username)
            self.browser.find_element_by_xpath(
                '//*[@id="pass"]').send_keys(password)
            self.browser.find_element_by_xpath('//*[@id="loginbutton"]').click()
            # self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#navItem_4748854339 > a:nth-child(2) > div:nth-child(2)')))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '._5qtp')))
            print('login successfully')

        except:
            print('Error correction')
            self.browser.refresh()
            time.sleep(5)
            self.main()

    def get_cookies(self):
        cookies = self.browser.get_cookies()
        jsonCookies = json.dumps(cookies)
        conn.ping(reconnect=True)
        cursor = conn.cursor()
        sql = "update {} SET cookie=%s  WHERE domain='facebookcorewwwi.onion' ".format(cookie_table)
        cursor.execute(sql, [jsonCookies])
        conn.commit()
        cursor.close()
        conn.close()
        return jsonCookies

    def main(self):
        self.login_url()
        self.login()
        self.get_cookies()
        self.browser.quit()

if __name__ == '__main__':
    testspider = Login()
    testspider.main()