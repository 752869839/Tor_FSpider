# -*- coding: utf-8 -*-
import json
import scrapy
import langid
import chardet
import logging
import urllib.parse
from datetime import datetime
from scrapy import Request
from tor_spider.items import HtmlItem

logger = logging.getLogger(__name__)
class DarkSpider(scrapy.Spider):
    name = 'onion_cryptbbs_bbs_spider'
    # allowed_domains = ['cryptbb2gezhohku.onion']
    start_urls = ['http://cryptbb2gezhohku.onion/']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'cryptbb2gezhohku.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        },
        'ITEM_PIPELINES': {
            'tor_spider.pipelines.TorDataPipeline': 188,
            'tor_spider.pipelines.DownloadImagesPipeline': 110,
            # 'scrapy_redis.pipelines.RedisPipeline': 100,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'tor_spider.middlewares.IpProxyDownloadMiddleware': 300,
            'tor_spider.middlewares.SocksProxyDownloadMiddleware': 300,
            'tor_spider.middlewares.Cryptbbs_LoginMiddleware': 100,
            'tor_spider.middlewares.Cryptbbs_CookieMiddleware': 400,
        },
        'DOWNLOAD_HANDLERS': {
            'http': 'tor_spider.handlers.Socks5DownloadHandler',
            'https': 'tor_spider.handlers.Socks5DownloadHandler',
        },
        'DOWNLOAD_DELAY' : 1
    }

    def parse(self, response):
        logger.info('开始采集!!!')
        item = HtmlItem()
        list_urls = response.xpath('//div[@id="tab_nav"]//a/@href').extract()
        for url in list_urls:
            url = response.urljoin(url)
            logger.info('主页链接')
            logger.info(url)
            yield Request(url, callback=self.parse_sencond,meta={'item': item})

    def parse_sencond(self, response):
        logger.info('请求状态码')
        logger.info(response.status)
        item = response.meta['item']
        try:
            img_url_list = []
            img_urls = response.xpath('//img/@src').extract()
            for img_url in img_urls:
                img_url = response.urljoin(img_url)
                img_url_list.append(img_url)
            item['img_url'] = img_url_list
        except Exception as e:
            pass

        item['url'] = str(response.url)
        item['domain'] = urllib.parse.urlparse(response.url).netloc
        item['title'] = response.xpath('//html/head/title/text()').extract_first()
        try:
            item['html'] = str(response.body, encoding='utf-8')
        except:
            item['html'] = response.body.decode("utf", "ignore")
        item['language'] = langid.classify(response.body)[0]
        encoding = chardet.detect(response.body)
        for key, value in encoding.items():
            if key == 'encoding' and not value is None:
                item['encode'] = value

        item['crawl_time'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        yield item

        try:
            details_urls = response.xpath(
                '//table[@class="tborder"]//a/@href').extract()
            for detail_url in details_urls:
                detail_url = response.urljoin(detail_url)
                logger.info('详情链接')
                logger.info(detail_url)
                yield Request(detail_url, callback=self.parse_third,meta={'item': item})
        except Exception as e:
            pass


    def parse_third(self,response):
        logger.info('请求状态码')
        logger.info(response.status)
        item = response.meta['item']
        try:
            img_url_list = []
            img_urls = response.xpath('//img/@src').extract()
            for img_url in img_urls:
                img_url = response.urljoin(img_url)
                img_url_list.append(img_url)
            item['img_url'] = img_url_list
        except Exception as e:
            pass

        item['url'] = str(response.url)
        item['domain'] = urllib.parse.urlparse(response.url).netloc
        item['title'] = response.xpath('//html/head/title/text()').extract_first()
        try:
            item['html'] = str(response.body, encoding='utf-8')
        except:
            item['html'] = response.body.decode("utf", "ignore")
        item['language'] = langid.classify(response.body)[0]
        encoding = chardet.detect(response.body)
        for key, value in encoding.items():
            if key == 'encoding' and not value is None:
                item['encode'] = value

        item['crawl_time'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        yield item

        try:
            details_urls = response.xpath(
                '//tr[@class="inline_row"]//a/@href').extract()
            for detail_url in details_urls:
                detail_url = response.urljoin(detail_url)
                logger.info('详情链接')
                logger.info(detail_url)
                yield Request(detail_url, callback=self.parse_fourth,meta={'item': item})
        except Exception as e:
            pass

        try:
            next_page = response.xpath('//a[text()= "Next »"]/@href').extract()[0]
            next_page = response.urljoin(next_page)
            logger.info('翻页链接')
            logger.info(next_page)
            yield Request(next_page, callback=self.parse_third,meta={'item': item})
        except Exception as e:
            pass


    def parse_fourth(self, response):
        logger.info('请求状态码')
        logger.info(response.status)
        item = response.meta['item']
        try:
            img_url_list = []
            img_urls = response.xpath('//img/@src').extract()
            for img_url in img_urls:
                img_url = response.urljoin(img_url)
                img_url_list.append(img_url)
            item['img_url'] = img_url_list
        except Exception as e:
            pass

        item['url'] = str(response.url)
        item['domain'] = urllib.parse.urlparse(response.url).netloc
        item['title'] = response.xpath('//html/head/title/text()').extract_first()
        try:
            item['html'] = str(response.body, encoding='utf-8')
        except:
            item['html'] = response.body.decode("utf", "ignore")
        item['language'] = langid.classify(response.body)[0]
        encoding = chardet.detect(response.body)
        for key, value in encoding.items():
            if key == 'encoding' and not value is None:
                item['encode'] = value

        item['crawl_time'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        yield item

        try:
            users = response.xpath('//dic[@class="author_avatar"]/a/@href').extract()
            for user in users:
                user = response.urljoin(user)
                logger.info('人物链接')
                logger.info(user)
                yield Request(user, callback=self.parse_fifth, meta={'item': item})
        except Exception as e:
            pass

        try:
            next_page = response.xpath('//a[text()= "Next »"]/@href').extract()[0]
            next_page = response.urljoin(next_page)
            logger.info('翻页链接')
            logger.info(next_page)
            yield Request(next_page, callback=self.parse_fourth,meta={'item': item})
        except Exception as e:
            pass



    def parse_fifth(self, response):
        logger.info('请求状态码')
        logger.info(response.status)
        item = response.meta['item']
        try:
            img_url_list = []
            img_urls = response.xpath('//img/@src').extract()
            for img_url in img_urls:
                img_url = response.urljoin(img_url)
                img_url_list.append(img_url)
            item['img_url'] = img_url_list
        except Exception as e:
            pass

        item['url'] = str(response.url)
        item['domain'] = urllib.parse.urlparse(response.url).netloc
        item['title'] = response.xpath('//html/head/title/text()').extract_first()
        try:
            item['html'] = str(response.body, encoding='utf-8')
        except:
            item['html'] = response.body.decode("utf", "ignore")
        item['language'] = langid.classify(response.body)[0]
        encoding = chardet.detect(response.body)
        for key, value in encoding.items():
            if key == 'encoding' and not value is None:
                item['encode'] = value

        item['crawl_time'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        yield item
