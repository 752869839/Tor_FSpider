# -*- coding: utf-8 -*-
import json
import langid
import chardet
import logging
from datetime import datetime
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from tor_spider.items import HtmlItem

logger = logging.getLogger(__name__)
class DarkSpider(RedisSpider):
    name = 'onion_agarth_market_spider'
    # allowed_domains = ['agarthaangodtcz3.onion']
    # start_urls = ['http://agarthaangodtcz3.onion/']
    redis_key = "agarth:start_url"

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS' : {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'agarthaangodtcz3.onion',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
    },
        'ITEM_PIPELINES' : {
            'tor_spider.pipelines.DownloadImagesPipeline': 110,
            'scrapy_redis.pipelines.RedisPipeline': 100,
},
        'DOWNLOADER_MIDDLEWARES' : {
            'tor_spider.middlewares.IpProxyDownloadMiddleware': 300,
            # 'tor_spider.middlewares.SocksProxyDownloadMiddleware': 300,
            'tor_spider.middlewares.Agarth_LoginMiddleware': 100,
            'tor_spider.middlewares.Agarth_CookieMiddleware': 400,
         },
        # 'DOWNLOAD_HANDLERS': {
        #     'http': 'tor_spider.handlers.Socks5DownloadHandler',
        #     'https': 'tor_spider.handlers.Socks5DownloadHandler',
        # },
    }

    def parse(self, response):
        logger.info('开始采集!!!')
        item = HtmlItem()
        list_urls = response.xpath('//div[@class="leftmenu-element cat_a_master "]/div/div/a/@href').extract()
        for list_url in list_urls:
            list_url = response.urljoin(list_url)
            logger.info('列表链接')
            logger.info(list_url)
            yield Request(list_url, callback=self.parse_second, meta={'item': item})

    def parse_second(self, response):
        logger.info('请求状态码')
        logger.info(response.status)
        item = response.meta['item']
        try:
            l_img = []
            imgs = response.xpath('//img/@src').extract()
            for i in imgs:
                img = response.urljoin(i)
                l_img.append(img)
            item['img'] = l_img
            item['html'] = str(response.body, encoding='utf-8')
        except Exception as e:
            pass
        details_urls = response.xpath('//tr[@class="products-list-item"]/td[4]/a/@href|//tr[@class="products-list-item"]/td[1]/a/@href').extract()
        for details_url in details_urls:
            details_url = response.urljoin(details_url)
            logger.info('详情链接')
            logger.info(details_url)
            yield Request(details_url, callback=self.parse_third, meta={'item': item})

        try:
            next_page = response.xpath('//a[text()="»"]/@href').extract()[0]
            next_page = response.urljoin(next_page)
            print('next_page:',next_page)
            yield Request(next_page, callback=self.parse_second,meta={'item': item})
        except Exception as e:
            pass

    def parse_third(self, response):
        logger.info('请求状态码')
        logger.info(response.status)
        item = response.meta['item']
        try:
            l_img = []
            imgs = response.xpath('//img/@src').extract()
            for i in imgs:
                img = response.urljoin(i)
                l_img.append(img)
            item['img'] = l_img
            item['html'] = str(response.body, encoding='utf-8')
        except Exception as e:
            pass
        item['crawl_time'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        item['net_type'] = 'tor'
        item['url'] = str(response.url)
        item['h1'] = response.xpath('//h1/text()').extract_first()
        item['raw_title'] = response.xpath('//html/head/title/text()').extract_first()
        item['meta'] = response.xpath('//*[@name="description"]/@content').extract_first()
        headers = dict(response.request.headers)
        info = {}
        for key, value in headers.items():
            new_key = str(key, encoding='utf-8')
            if isinstance(value, list):
                new_value = [str(x, encoding='utf-8') for x in value]
            else:
                new_value = str(value, encoding='utf-8')
            info[new_key] = new_value
        item['headers'] = json.dumps(info)
        item['raw_text'] = str(response.body, encoding='utf-8')
        item['domain'] = 'agarthaangodtcz3.onion'
        item['language'] = langid.classify(response.body)[0]
        item['content_type'] = 'text/html; charset=utf-8'
        a = chardet.detect(response.body)
        for key, value in a.items():
            if key == 'encoding':
                item['content_encode'] = value

        item['code'] = response.status
        elements = response.xpath('//a')
        links = []
        for el in elements:
            url = ""
            name = ""
            urls = el.xpath("@href").extract()
            if len(urls) > 0:
                url = urls[0]
            names = el.xpath("@title|text()|@name").extract()
            if len(names) > 0:
                name = names[0].strip()
            dict1 = {
                "link": url,
                "name": name
            }
            if not dict in links:
                links.append(dict1)
                item['links'] = links
        yield item







