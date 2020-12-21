# -*- coding: utf-8 -*-
import re
import json
import scrapy
import chardet
import langid
import logging
import urllib.parse
from scrapy import Request
from datetime import datetime
from tor_spider.items import HtmlItem

logger = logging.getLogger(__name__)
class DarkSpider(scrapy.Spider):
    name = 'onion_alibaba_market_spider'
    # allowed_domains = ['alibaba2kw6qoh6o.onion']
    start_urls = ['http://alibaba2kw6qoh6o.onion/']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS' : {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'alibaba2kw6qoh6o.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
    },
        'ITEM_PIPELINES' : {
            'tor_spider.pipelines.TorDataPipeline': 188,
            'tor_spider.pipelines.DownloadImagesPipeline': 110,
            # 'scrapy_redis.pipelines.RedisPipeline': 100,
},
        'DOWNLOADER_MIDDLEWARES' : {
            # 'tor_spider.middlewares.IpProxyDownloadMiddleware': 300,
            'tor_spider.middlewares.SocksProxyDownloadMiddleware': 300,
            'tor_spider.middlewares.Alibaba_LoginMiddleware': 100,
            'tor_spider.middlewares.Alibaba_CookieMiddleware': 400,
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
        list_urls = response.xpath('//div[@class="flex-fill float-left"]/a/@href').extract()
        for list_url in list_urls[1:2]:
            list_url = response.urljoin(list_url)
            logger.info('主页列表页链接')
            logger.info(list_url)
            yield Request(list_url, callback=self.parse_sencond, meta={'item': item})

    def parse_sencond(self, response):
        logger.info('请求状态码')
        logger.info(response.status)
        item = response.meta['item']
        try:
            next_pages = response.xpath('//ul[@class="pagination text-center"]/li[last()]/a/@href').extract()[0]
            pg = re.findall(r'page=([\s|\S]+)',next_pages)[0]
            for i in range(1,int(pg)):
            #for i in range(1,3):
                next_page = response.url+'?page={}'.format(i)
                # logger.info('翻页链接')
                # logger.info(next_page)
                yield Request(next_page, callback=self.parse_next_page, meta={'item': item})
        except Exception as e:
            pass

    def parse_next_page(self,response):
        logger.info('翻页链接')
        logger.info(response.url)
        logger.info('请求状态码')
        logger.info(response.status)
        item = response.meta['item']
        list_urls = response.xpath('//div[@class="col-md-6 pt-3 pl-md-3 pr-md-3"]/a/@href').extract()
        for list_url in list_urls:
            list_url = response.urljoin(list_url)
            # logger.info('商品详情链接')
            # logger.info(list_url)
            yield Request(list_url, callback=self.parse_third, meta={'item': item})

    def parse_third(self,response):
        logger.info('商品详情链接')
        logger.info(response.url)
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




