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
    name = 'onion_nytime_new_spider'
    # allowed_domains = ['nytimes3xbfgragh.onion']
    start_urls = ['https://cn.nytimes3xbfgragh.onion/']

    custom_settings = {
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
        'DOWNLOAD_DELAY' : 1
    }

    def parse(self,response):
        logger.info('开始采集!!!')
        item = HtmlItem()
        urls = response.xpath('//li[@class="mainSection  drop"]/a/@href|//li[@class="mainSection "]/a/@href').extract()
        for url in urls:
            url = response.urljoin(url)
            logger.info(f'新闻类目链接:{url}')
            yield Request(url, callback=self.parse_second, meta={'item': item})

    def parse_second(self,response):
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

        try:
            next_page = response.xpath('//a[text()="下一页 >>"]/@href').extract()[0]
            next_page = response.urljoin(next_page)
            logger.info(f'翻页链接:{next_page}')
            yield Request(next_page, callback=self.parse_second, meta={'item': item})
        except Exception as e:
            pass

        details_urls = response.xpath('//h3[@class="regularSummaryHeadline"]/a/@href').extract()
        for details_url in details_urls:
            details_url = response.urljoin(details_url)
            logger.info(f'详情链接:{details_url}')
            yield Request(details_url, callback=self.parse_third, meta={'item': item})

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
