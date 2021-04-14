# -*- coding: utf-8 -*-
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
    name = 'onion_zj4o7_market_spider'
    # allowed_domains = ['7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion']
    start_urls = ['http://7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion/user']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': '7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
        },
        'ITEM_PIPELINES': {
            'tor_spider.pipelines.TorDataPipeline': 188,
            # 'tor_spider.pipelines.DownloadImagesPipeline': 110,
            # 'scrapy_redis.pipelines.RedisPipeline': 100,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'tor_spider.middlewares.IpProxyDownloadMiddleware': 300,
            'tor_spider.middlewares.SocksProxyDownloadMiddleware': 300,
            'tor_spider.middlewares.Zj4o7_LoginMiddleware': 100,
            'tor_spider.middlewares.Zj4o7_CookieMiddleware': 400,
        },
        'DOWNLOAD_HANDLERS': {
            'http': 'tor_spider.handlers.Socks5DownloadHandler',
            'https': 'tor_spider.handlers.Socks5DownloadHandler',
        },
        'DOWNLOAD_DELAY' : 1.5
    }


    def parse(self, response):
        logger.info('开始采集!!!')
        item = HtmlItem()
        list_urls = response.xpath('//div[@id="sidebar-menu"]/ul/li[last()]/a/@href').extract()
        for list_url in list_urls:
            list_url = response.urljoin(list_url)
            logger.info(f'首页链接:  {list_url}')
            yield Request(list_url, callback=self.parse_sencond, meta={'item': item})

    def parse_sencond(self, response):
        logger.info(f'请求状态码:  {response.status}')
        item = response.meta['item']
        # list_urls = response.xpath('//div[@class="content s2" or @class="more"]//a/@href|//div[@class="card-header"]//a/@href').extract()
        list_urls = response.xpath('//div[@class="content s2"]//a/@href|//div[@class="card-header"]//a/@href').extract()
        for list_url in list_urls:
            list_url = response.urljoin(list_url)
            logger.info(f'查看更多链接:  {list_url}')
            yield Request(list_url, callback=self.parse_third, meta={'item': item})


        more_url = response.xpath('//div[@class="more"]/a/@href').extract()[0]
        more_url = response.urljoin(more_url)
        yield Request(more_url, callback=self.parse_third, meta={'item': item})


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
        item['html'] = response.body.decode("utf", "ignore")
        item['language'] = langid.classify(response.body)[0]
        encoding = chardet.detect(response.body)
        for key, value in encoding.items():
            if key == 'encoding' and not value is None:
                item['encode'] = value

        item['crawl_time'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        yield item

        try:
            details_urls = response.xpath('//div[@class="col-md-3 shop " or @class="col-md-3 shop shop0"]/a/@href|//div[@class="subject break-all"]/a/@href').extract()
            for details_url in details_urls:
                details_url = response.urljoin(details_url)
                logger.info(f'商品和帖子链接:  {details_url}')
                yield Request(details_url, callback=self.parse_fourth, meta={'item': item})
        except Exception as e:
            pass

        try:
            next_page = response.xpath('//a[text()="下一页"]/@href').extract()[0]
            if "#" not in next_page:
                logger.info(f'翻页链接:  {next_page}')
                next_page = response.urljoin(next_page)
                yield Request(next_page, callback=self.parse_third, meta={'item': item})
        except:
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

        try:
            shop_urls = response.xpath('//a[@class="btn btn-primary"]/@href').extract()
            for shop_url in shop_urls:
                shop_url = response.urljoin(shop_url)
                logger.info(f'店铺链接:  {shop_url}')
                yield Request(shop_url, callback=self.parse_fifth, meta={'item': item})
        except Exception as e:
            pass

    def parse_fifth(self, response):
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
