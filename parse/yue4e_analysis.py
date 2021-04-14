# -*- coding: utf-8 -*-
import re
import time
from lxml import etree
from datetime import datetime
from dateutil.relativedelta import relativedelta
from elasticsearch6.helpers import bulk, scan
import sim_hash
from config import es
from bit_eth_ema import bitcoin_extract,eth_extract,email_extract
from mylog import logger, exception_logger

logger = logger()

class Analysis(object):
    def exquisite(self):
        search_query = {
            "query": {
                "match_phrase": {
                    "domain": {
                        "query": "yue4eifx522t5zjb.onion"
                    }
                }
            }
        }

        res = scan(client=es, query=search_query, scroll='5m', index='page', doc_type='_doc', timeout='5m')
        cnt = 0
        for record in res:
            print(cnt, record["_source"]["url"])
            cnt += 1
            html = record["_source"]["raw_text"]
            response = etree.HTML(html)
            try:

                if record["_source"]["url"][0:37] == 'http://yue4eifx522t5zjb.onion/product':

                    crawl_time = record["_source"]["crawl_time"]

                    domain = 'yue4eifx522t5zjb.onion'

                    net_type = 'tor'

                    spider_name = 'onion_yue4e_market_spider'

                    try:
                        goods_name = response.xpath('//h1[@class="product_title entry-title"]/text()')[0].strip()
                        print(goods_name)
                    except:
                        goods_name = ''

                    try:
                        goods_id = response.xpath('//h1[@class="product_title entry-title"]/text()')[0].strip()
                    except:
                        goods_id = ''

                    url = record["_source"]["url"]

                    try:
                        goods_info = ''
                        info = response.xpath('//div[@class="item-details"]//text()')
                        for i in info:
                            goods_info += i
                    except:
                        goods_info = ''

                    try:
                        goods_img_url = response.xpath(
                            '//a[@class="woocommerce-main-image "]/@href')  # 图片
                        print(goods_img_url)
                    except:
                        goods_img_url = []

                    try:
                        crawl_category = response.xpath('//div[@class="item-category left"]/a/text()')[0].strip()
                    except:
                        crawl_category = ''

                    try:
                        sold_count = re.findall('span>(.*?) 销售量', html)[0]
                        sold_count = int(sold_count)
                    except:
                        sold_count = None

                    try:
                        price = response.xpath(
                            '//meta[@itemprop="price"]/@content')
                        price = [i + '$' for i in price]
                    except:
                        price = []

                    try:
                        user_id = response.xpath('//h1[@class="product_title entry-title"]/text()')[0].strip()
                    except:
                        user_id = ''

                    try:
                        user_name = response.xpath('//h1[@class="product_title entry-title"]/text()')[0].strip()
                    except:
                        user_name = ''

                    goods_area = ''
                    raw_publish_time = ''
                    publish_time = None
                    sku = ''

                    bitcoin_addresses = bitcoin_extract(goods_info)

                    eth_addresses = eth_extract(goods_info)

                    id = sim_hash.g_id(spider_name, goods_id)
                    actions = [{
                        "_index": 'goods',
                        "_type": '_doc',
                        "_op_type": 'create',
                        "_id": id,
                        "_source": {
                            "crawl_time": crawl_time,
                            "domain": domain,
                            "net_type": net_type,
                            "spider_name": spider_name,
                            "goods_name": goods_name,
                            "goods_id": goods_id,
                            "url": url,
                            "goods_info": goods_info,
                            "goods_img_url": goods_img_url,
                            "crawl_category": crawl_category,
                            "sold_count": sold_count,
                            "price": price,
                            "user_id": user_id,
                            "user_name": user_name,
                            "goods_area": goods_area,
                            "raw_publish_time": raw_publish_time,
                            "publish_time": publish_time,
                            "sku": sku,
                            "bitcoin_addresses": bitcoin_addresses,
                            "eth_addresses": eth_addresses,
                            "gmt_create": record["_source"]["gmt_create"],
                            "gmt_modified": record["_source"]["gmt_modified"],
                        }
                    }]
                    success, _ = bulk(es, actions, index='goods', raise_on_exception=False, raise_on_error=False)



                # topic
                if record["_source"]["url"][0:37] == 'http://yue4eifx522t5zjb.onion/answers':

                    spider_name = 'onion_yue4e_market_spider'

                    domain = 'yue4eifx522t5zjb.onion'

                    url = record["_source"]["url"]

                    page_index_id = record["_id"]

                    net_type = 'tor'

                    topic_type = 'post'

                    crawl_tags = ['互动空间']

                    try:
                        title = response.xpath('//h1[@class="entry-title"]/text()')[0]
                    except:
                        title = ''

                    try:
                        topic_id = response.xpath('//h1[@class="entry-title"]/text()')[0]
                    except:
                        topic_id = ''

                    try:
                        user_id = response.xpath('//div[@class="cma-question-author"]/text()')[0]
                        user_id = re.findall(r'Posted by ([\s|\S]+)', user_id)[0]
                    except:
                        user_id = ''

                    try:
                        user_name = response.xpath('//div[@class="cma-question-author"]/text()')[0]
                        user_name = re.findall(r'Posted by ([\s|\S]+)', user_id)[0]
                    except:
                        user_name = ''

                    commented_user_id = ''
                    comment_id = ''

                    try:
                        raw_content = response.xpath('//div[@class="cma-question-body"]')[0]
                        raw_content = etree.tostring(raw_content, encoding='utf-8')
                        raw_content = str(raw_content, encoding='utf-8')
                    except:
                        raw_content = ''

                    try:
                        contents = response.xpath('//div[@class="cma-question-body"]')
                        content = contents[0].xpath('string(.)')
                    except:
                        content = ''

                    clicks_times = None
                    commented_times = None

                    crawl_time = record["_source"]["crawl_time"]

                    try:
                        raw_publish_time = response.xpath('//div[@class="cma-question-date"]/text()')[0].strip()
                        raw_publish_time = re.findall(r'Asked on ([\s|\S]+)', raw_publish_time)[0]
                    except:
                        raw_publish_time = ''

                    try:
                        publish_time = datetime.strptime(raw_publish_time, '%Y年%m月%d日 %H:%M')
                        publish_time = publish_time - relativedelta(hours=8)
                    except:
                        publish_time = None

                    thumbs_up = None
                    thumbs_down = None

                    emails = email_extract(content)

                    bitcoin_addresses = bitcoin_extract(content)

                    eth_addresses = eth_extract(content)

                    id = sim_hash.t_id(spider_name, topic_id, user_id, raw_content, comment_id)
                    actions = [{
                        "_index": 'topic',
                        "_type": '_doc',
                        "_op_type": 'create',
                        "_id": id,
                        "_source": {
                            "spider_name": spider_name,
                            "domain": domain,
                            "url": url,
                            "page_index_id": page_index_id,
                            "net_type": net_type,
                            "topic_type": topic_type,
                            "crawl_tags": crawl_tags,
                            "title": title,
                            "topic_id": topic_id,
                            "user_id": user_id,
                            "user_name": user_name,
                            # "commented_user_id": commented_user_id,
                            # "comment_id": comment_id,
                            "raw_content": raw_content,
                            "content": content,
                            "clicks_times": clicks_times,
                            "commented_times": commented_times,
                            "crawl_time": crawl_time,
                            "publish_time": publish_time,
                            "raw_publish_time": raw_publish_time,
                            "thumbs_up": thumbs_up,
                            "thumbs_down": thumbs_down,
                            "emails": emails,
                            "bitcoin_addresses": bitcoin_addresses,
                            "eth_addresses": eth_addresses,
                            "gmt_create": record["_source"]["gmt_create"],
                            "gmt_modified": record["_source"]["gmt_modified"],
                        }
                    }]
                    success, _ = bulk(es, actions, index='topic', raise_on_exception=False, raise_on_error=False)


                    p = response.xpath('//div[@id="content"]/table')
                    if len(p) > 1:
                        poster_list = response.xpath('//div[@id="content"]/table')
                        poster_lenght = len(poster_list)
                        for index in range(1, poster_lenght):
                            poster = poster_list[index]

                            spider_name = 'onion_yue4e_market_spider'

                            domain = 'yue4eifx522t5zjb.onion'

                            url = record["_source"]["url"]

                            page_index_id = record["_id"]

                            net_type = 'tor'

                            topic_type = 'comment'

                            crawl_tags = ['互动空间']

                            try:
                                title = response.xpath('//h1[@class="entry-title"]/text()')[0]
                            except:
                                title = ''

                            try:
                                topic_id = response.xpath('//h1[@class="entry-title"]/text()')[0]
                            except:
                                topic_id = ''

                            try:
                                user_id = poster.xpath('tr//div[@class="cma-answer-author"]/text()')[0]
                                user_id = re.findall(r'Posted by ([\s|\S]+)', user_id)[0]
                            except:
                                user_id = ''

                            try:
                                user_name = poster.xpath('tr//div[@class="cma-answer-author"]/text()')[0]
                                user_name = re.findall(r'Posted by ([\s|\S]+)', user_id)[0]
                            except:
                                user_name = ''

                            try:
                                commented_user_id = response.xpath('//div[@class="cma-question-author"]/text()')[0]
                                commented_user_id = re.findall(r'Posted by ([\s|\S]+)', user_id)[0]
                            except:
                                commented_user_id = ''

                            comment_id = ''

                            try:
                                raw_content = poster.xpath('tr//div[@class="cma-answer-body"]/p')[0]
                                raw_content = etree.tostring(raw_content, encoding='utf-8')
                                raw_content = str(raw_content, encoding='utf-8')
                            except:
                                raw_content = ''

                            try:
                                contents = poster.xpath('tr//div[@class="cma-answer-body"]/p')
                                content = contents[0].xpath('string(.)')
                                print(content)
                            except:
                                content = ''

                            clicks_times = None
                            commented_times = None

                            crawl_time = record["_source"]["crawl_time"]

                            try:
                                raw_publish_time = poster.xpath('tr//div[@class="cma-answer-date"]/text()')[0]
                                raw_publish_time = re.findall(r'Answered On ([\s|\S]+)', raw_publish_time)[0]
                            except:
                                raw_publish_time = ''

                            try:
                                publish_time = datetime.strptime(raw_publish_time, '%Y年%m月%d日 %H:%M')
                                publish_time = publish_time - relativedelta(hours=8)
                            except:
                                publish_time = None

                            thumbs_up = None
                            thumbs_down = None

                            emails = email_extract(content)

                            bitcoin_addresses = bitcoin_extract(content)

                            eth_addresses = eth_extract(content)

                            id = sim_hash.t_id(spider_name, topic_id, user_id, raw_content, comment_id)
                            actions = [{
                                "_index": 'topic',
                                "_type": '_doc',
                                "_op_type": 'create',
                                "_id": id,
                                "_source": {
                                    "spider_name": spider_name,
                                    "domain": domain,
                                    "url": url,
                                    "page_index_id": page_index_id,
                                    "net_type": net_type,
                                    "topic_type": topic_type,
                                    "crawl_tags": crawl_tags,
                                    "title": title,
                                    "topic_id": topic_id,
                                    "user_id": user_id,
                                    "user_name": user_name,
                                    "commented_user_id": commented_user_id,
                                    "comment_id": comment_id,
                                    "raw_content": raw_content,
                                    "content": content,
                                    "clicks_times": clicks_times,
                                    "commented_times": commented_times,
                                    "crawl_time": crawl_time,
                                    "publish_time": publish_time,
                                    "raw_publish_time": raw_publish_time,
                                    # "thumbs_up": thumbs_up,
                                    # "thumbs_down": thumbs_down,
                                    "emails": emails,
                                    "bitcoin_addresses": bitcoin_addresses,
                                    "eth_addresses": eth_addresses,
                                    "gmt_create": record["_source"]["gmt_create"],
                                    "gmt_modified": record["_source"]["gmt_modified"],
                                }
                            }]
                            success, _ = bulk(es, actions, index='topic', raise_on_exception=False, raise_on_error=False)

            except Exception as e:
                logger.warning(e)

if __name__ == '__main__':
    a = Analysis()
    a.exquisite()