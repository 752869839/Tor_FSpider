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
    name = 'onion_xs6qb_market_spider'
    # allowed_domains = ['xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion']
    start_urls = ['http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion/index.php']
    # http://xxxxxxxx3a3kuuhhw5w7stk25fzhttrlpiomij5bogkg7yyqsng5tqyd.onion/index.php

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion',
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
            'tor_spider.middlewares.Xs6qb_LoginMiddleware': 100,
            'tor_spider.middlewares.Xs6qb_CookieMiddleware': 400,
        },
        'DOWNLOAD_HANDLERS': {
            'http': 'tor_spider.handlers.Socks5DownloadHandler',
            'https': 'tor_spider.handlers.Socks5DownloadHandler',
        },
    }

    def parse(self, response):
        logger.info('开始采集!!!')
        item = HtmlItem()
        urls = response.xpath('//div[@class="length_308"]/a/@href|//a[@class="index_list_title"]/@href').extract()
        for url in urls:
            url = response.urljoin(url)
            logger.info(f'商品链接:  {url}')
            yield Request(url, callback=self.parse_second, meta={'item': item})

    def parse_second(self,response):
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
            details_urls = response.xpath('//div[@class="length_500"]/a/@href').extract()
            for details_url in details_urls:
                details_url = response.urljoin(details_url)
                logger.info(f'商品链接:{details_url}')
                yield Request(details_url, callback=self.parse_third, meta={'item': item})
        except Exception as e:
            pass

        if len(response.url) == 85:
            page = response.xpath('//span[@class="button_page"][last()]/text()').extract()
            print(page)
            p = ''
            for k in page:
                p = k.strip()
            p = int(p) + 1
            for next_page in range(0,p):
                next_page = response.url + '&pagea={}#pagea'.format(next_page)
                next_page = response.urljoin(next_page)
                logger.info(f'翻页链接:  {next_page}')
                yield Request(next_page, callback=self.parse_second,meta={'item': item})


    def parse_third(self,response):
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
