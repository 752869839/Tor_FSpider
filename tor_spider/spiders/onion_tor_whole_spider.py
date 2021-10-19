# -*- coding: utf-8 -*-
import re
import urllib
import langid
import chardet
import logging
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from tor_spider.items import TorWholeNetworkItem

logger = logging.getLogger(__name__)

class OnionTorWholeSpider(RedisCrawlSpider):
    name = 'onion_tor_whole_spider'
    redis_key = 'whole'
    # allowed_domains = ['onion']

    rules = [
        Rule(LinkExtractor(allow=('\.*onion.*'),
            # deny=('*video|*mp4|*png|*jpg'),
            restrict_xpaths=('//a[@href]')),
             callback='parse_item',
             follow=True)
    ]

    def __init__(self, *args, **kwargs):
        super(OnionTorWholeSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        item = TorWholeNetworkItem()
        try:
            img_url_list = []
            img_urls = response.xpath('//img/@src').extract()
            for img_url in img_urls:
                img_url = response.urljoin(img_url)
                if '.jpg' in img_url or '.png' in img_url:
                    img_url_list.append(img_url)
            item['img_url'] = img_url_list
        except:
            pass

        item['url'] = str(response.url)
        item['status'] = str(response.status)
        # item['domain'] = urllib.parse.urlparse(response.url).netloc
        if '-' in response.url[0:30]:
            domain = urllib.parse.urlparse(response.url).netloc
            item['domain'] = re.findall('\.([\s|\S]+)', domain)[0]
        else:
            item['domain'] = urllib.parse.urlparse(response.url).netloc

        try:
            item['title'] = response.xpath('//html/head/title/text()').extract_first()
        except:
            item['title'] = ''
        item['description'] = response.xpath('//*[@name="description"]/@content').extract_first()
        try:
            item['html'] = str(response.body, encoding='utf-8')
        except:
            item['html'] = response.body.decode("utf", "ignore")
        item['language'] = langid.classify(response.body)[0]

        encoding = chardet.detect(response.body)
        for key, value in encoding.items():
            if key == 'encoding' and not value is None:
                item['encode'] = value
            else:
                item['encode'] = ''

        item['crawl_time'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        logger.info(response.url)
        yield item


