# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HtmlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    crawl_time = scrapy.Field()
    net_type = scrapy.Field()
    url = scrapy.Field()
    h1 = scrapy.Field()
    raw_title = scrapy.Field()
    meta = scrapy.Field()
    headers = scrapy.Field()
    raw_text = scrapy.Field()
    domain = scrapy.Field()
    language = scrapy.Field()
    content_type = scrapy.Field()
    content_encode = scrapy.Field()
    code = scrapy.Field()
    links = scrapy.Field()
    picture = scrapy.Field()
    picture2 = scrapy.Field()
    user_id = scrapy.Field()
    goods_id = scrapy.Field()
    img = scrapy.Field()
    html = scrapy.Field()






