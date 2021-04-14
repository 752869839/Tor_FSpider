# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HtmlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    img = scrapy.Field()
    url = scrapy.Field()
    domain = scrapy.Field()
    title = scrapy.Field()
    html = scrapy.Field()
    language = scrapy.Field()
    encode = scrapy.Field()
    crawl_time = scrapy.Field()






