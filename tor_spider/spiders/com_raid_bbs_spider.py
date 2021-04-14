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
    name = 'com_raid_bbs_spider'
    # allowed_domains = ['raidforums.com/]
    start_urls = ['https://raidforums.com/']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
            'authority': 'raidforums.onion',
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
            'tor_spider.middlewares.VSocksProxyDownloadMiddleware': 300,
        },
        'DOWNLOAD_HANDLERS': {
            'http': 'tor_spider.handlers.Socks5DownloadHandler',
            'https': 'tor_spider.handlers.Socks5DownloadHandler',
        },
        'DOWNLOAD_DELAY' : 0.5
    }

    def parse(self, response):
        logger.info('开始采集!!!')
        item = HtmlItem()
        list_urls = response.xpath('//ul[@class="forum-tabs__tabs nav talign-mleft"]/li/a/@href').extract()
        for list_url in list_urls:
            list_url = response.urljoin(list_url)
            logger.info(f'主页列表页链接:{list_url}')
            yield Request(list_url, callback=self.parse_sencond, meta={'item': item})

    def parse_sencond(self, response):
        logger.info(f'请求状态码:{response.status}')
        item = response.meta['item']
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

        list_urls = response.xpath('//a[@class="forums__forum-name"]/@href').extract()
        for list_url in list_urls:
            list_url = response.urljoin(list_url)
            logger.info(f'二级页面链接: {list_url}')
            yield Request(list_url, callback=self.parse_third, meta={'item': item})

    def parse_third(self,response):
        logger.info(f'请求状态码:{response.status}')
        item = response.meta['item']
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

        try:
            detail_urls = response.xpath('//a[@class="forum-display__thread-name"]/@href').extract()
            for url in detail_urls:
                url = response.urljoin(url)
                logger.info(f'详情链接:{url}')
                yield Request(url, callback=self.parse_fourth, meta={'item': item})
        except Exception as e:
            logger.info(e)

        try:
            next_page = response.xpath('//a[text()= "Next »"]/@href').extract()[0]
            next_page = response.urljoin(next_page)
            logger.info(f'翻页链接:  {next_page}')
            yield Request(next_page, callback=self.parse_third, meta={'item': item})
        except Exception as e:
            pass

    def parse_fourth(self, response):
        logger.info(f'请求状态码:  {response.status}')
        item = response.meta['item']
        imgs = response.xpath('//img/@src').extract()
        if len(imgs) > 0:
            l_img = []
            for i in imgs:
                img = response.urljoin(i)
                l_img.append(img)
            item['img'] = l_img
            item['html'] = str(response.body, encoding='utf-8')
        else:
            pass
        item['url'] = str(response.url)
        item['domain'] = urllib.parse.urlparse(response.url).netloc
        item['title'] = response.xpath('//html/head/title/text()').extract_first()
        item['html'] = response.body.decode("utf", "ignore")
        item['language'] = langid.classify(response.body)[0]
        encoding = chardet.detect(response.body)
        for key, value in encoding.items():
            if key == 'encoding' and not value is None:
                item['encode'] = value

        item['crawl_time'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        yield item

        # try:
        #     next_page = response.xpath('//a[text()= "Next »"]/@href').extract()[0]
        #     next_page = response.urljoin(next_page)
        #     logger.info(f'翻页链接:  {next_page}')
        #     yield Request(next_page, callback=self.parse_fourth, meta={'item': item})
        # except Exception as e:
        #     pass