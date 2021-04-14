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
    name = 'onion_yue4e_market_spider'
    # allowed_domains = ['yue4eifx522t5zjb.onion']
    start_urls = ['http://yue4eifx522t5zjb.onion/']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'yue4eifx522t5zjb.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        },
        'ITEM_PIPELINES': {
            'tor_spider.pipelines.TorDataPipeline': 188,
            'tor_spider.pipelines.DownloadImagesPipeline': 110,
            # 'scrapy_redis.pipelines.RedisPipeline': 100,
        },
        'DOWNLOADER_MIDDLEWARES' : {
            # 'tor_spider.middlewares.IpProxyDownloadMiddleware': 300,
            'tor_spider.middlewares.SocksProxyDownloadMiddleware': 300,
        },
        'DOWNLOAD_HANDLERS': {
            'http': 'tor_spider.handlers.Socks5DownloadHandler',
            'https': 'tor_spider.handlers.Socks5DownloadHandler',
        },
    }


    def parse(self, response):
        logger.info('开始采集!!!')
        item = HtmlItem()
        list_urls = response.xpath('//li[@id="menu-item-3643"]/ul/li[1]/a/@href|//li[@id="menu-item-3651"]/a/@href').extract()
        for list_url in list_urls:
            list_url = response.urljoin(list_url)
            print(list_url)
            yield Request(list_url, callback=self.parse_sencond, meta={'item': item})

    def parse_sencond(self, response):
        item = response.meta['item']
        list_urls = response.xpath('//div[@class="item-image fullwidth"]/div/a/@href|//div[@class="cma-thread-title"]/a/@href').extract()
        for list_url in list_urls:
            list_url = response.urljoin(list_url)
            logger.info(list_url)
            yield Request(list_url, callback=self.parse_third, meta={'item': item})

        try:
            next_page = response.xpath('//a[@class="next page-numbers"]/@href|//a[text()="下一页 »"]/@href').extract()[0]
            next_page = response.urljoin(next_page)
            logger.info(f'list_url,{list_url}')
            yield Request(next_page, callback=self.parse_sencond, meta={'item': item})
        except Exception as e:
            print(e)

    def parse_third(self,response):
        logger.info(f'请求状态码:{response.status}')
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
