# -*- coding: utf-8 -*-
import re
import json
import scrapy
import langid
import chardet
import logging
import urllib.parse
from scrapy import Request
from datetime import datetime
from tor_spider.items import HtmlItem

logger = logging.getLogger(__name__)
class DarkSpider(scrapy.Spider):
    name = 'onion_agarth_market_spider'
    # allowed_domains = ['agarthaangodtcz3.onion']
    start_urls = ['http://agartha2oooh2cxa.onion/']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS' : {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'agartha2oooh2cxa.onion',
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
            # 'tor_spider.middlewares.Agarth_LoginMiddleware': 100,
            # 'tor_spider.middlewares.Agarth_CookieMiddleware': 400,
         },
        'DOWNLOAD_HANDLERS': {
            'http': 'tor_spider.handlers.Socks5DownloadHandler',
            'https': 'tor_spider.handlers.Socks5DownloadHandler',
        },
        'DOWNLOAD_DELAY': 0.1
    }

    def parse(self, response):
        logger.info('开始采集!!!')
        item = HtmlItem()
        list_urls = response.xpath('//td[@class="info"]/a/@href').extract()
        for list_url in list_urls:
            list_url = response.urljoin(list_url)
            logger.info(f'列表链接:{list_url}')
            yield Request(list_url, callback=self.parse_second, meta={'item': item})

    def parse_second(self, response):
        logger.info(f'请求状态码:{response.status}')
        item = response.meta['item']
        details_urls = response.xpath('//td[@class="subject windowbg2"]/div/span/a/@href').extract()
        for details_url in details_urls:
            details_url = response.urljoin(details_url)
            logger.info(f'详情链接:{details_url}')
            yield Request(details_url, callback=self.parse_third, meta={'item': item})

        try:
            end_page = response.xpath('//a[@class="navPages"][last()]/@href').extract()[0]
            boadr_int = re.findall('=(.*?)\.',end_page)[0]
            end_page = re.findall('=([\s|\S]+)',end_page)[0]
            end_page = re.findall('\.([\s|\S]+)', end_page)[0]
            end_page = int(end_page) + 20
            for page in range(20,end_page,20):
                next_page = f'http://agartha2oooh2cxa.onion/index.php?board={boadr_int}.{page}'
                logger.info(f'翻页链接:{next_page}')
                yield Request(next_page, callback=self.parse_second,meta={'item': item})
        except Exception as e:
            pass

    def parse_third(self, response):
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







