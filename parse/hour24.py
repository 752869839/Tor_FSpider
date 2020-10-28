# -*- coding: utf-8 -*-
import time
import re
from lxml import etree
from elasticsearch6.helpers import bulk, scan
import sim_hash
from logg import logger
from config import es
from bit_eth_ema import bitcoin_extract,eth_extract,email_extract

class Analysis(object):
    def exquisite(self):
        search_query = {
            "query": {
                "match_phrase": {
                    "domain": {
                        "query": "24hourspkcmd7bvr.onion"
                    }
                }
            }
        }

        res = scan(client=es, query=search_query, scroll='10m', index='page', doc_type='_doc', timeout='5m')
        cnt = 0
        for record in res:
            print(cnt, record["_source"]["url"])
            cnt += 1
            html = record["_source"]["raw_text"]
            response = etree.HTML(html)
            try:
                # user
                if '.html' in record["_source"]["url"]:
                    spider_name = 'onion_hour24_market_spider'

                    domain = '24hourspkcmd7bvr.onion'

                    net_type = 'tor'

                    try:
                        user_id = re.findall(r'Company:</b></td><td>(.*?)</td>', html)[0].strip()
                        if user_id == '':
                            user_id = '24hour'
                    except:
                        user_id = '24hour'

                    user_description = ""

                    try:
                        user_name = re.findall(r'Company:</b></td><td>(.*?)</td>', html)[0].strip()
                        if user_name == '':
                            user_name = '24hour'
                    except:
                        user_name = '24hour'

                    url = record["_source"]["url"]
                    raw_register_time = ''
                    register_time = None
                    user_img_url = ''

                    emails = email_extract(user_description)

                    bitcoin_addresses = bitcoin_extract(user_description)

                    eth_addresses = eth_extract(user_description)

                    raw_last_active_time = ''
                    last_active_time = None
                    area = ''
                    ratings = ''
                    level = ''
                    member_degree = ''
                    pgp = ''

                    try:
                        crawl_time = record["_source"]["crawl_time"]
                    except:
                        crawl_time = ''

                    topic_nums = None
                    goods_orders = None
                    identity_tags = ''

                    id = sim_hash.u_id(spider_name, user_id)
                    actions = [{
                        "_index": 'user',
                        "_type": '_doc',
                        "_op_type": 'create',
                        "_id": id,
                        "_source": {
                            "spider_name": spider_name,
                            "domain": domain,
                            "net_type": net_type,
                            "user_name": user_name,
                            "user_description": user_description,
                            "user_id": user_id,
                            "url": url,
                            "raw_register_time": raw_register_time,
                            #"register_time": register_time,
                            "user_img_url": user_img_url,
                            "emails": emails,
                            "bitcoin_addresses": bitcoin_addresses,
                            "eth_addresses": eth_addresses,
                            "raw_last_active_time": raw_last_active_time,
                            #"last_active_time": last_active_time,
                            "area": area,
                            "ratings": ratings,
                            "level": level,
                            "member_degree": member_degree,
                            "pgp": pgp,
                            "crawl_time": crawl_time,
                            #"topic_nums": topic_nums,
                            #"goods_orders": goods_orders,
                            "identity_tags": identity_tags,
                            "gmt_create": record["_source"]["gmt_create"],
                            "gmt_modified": record["_source"]["gmt_modified"],
                        }
                    }]
                    success, _ = bulk(es, actions, index='user', raise_on_exception=False, raise_on_error=False)

                # goods
                if '.html' in record["_source"]["url"]:

                    crawl_time = record["_source"]["crawl_time"]
                    domain = '24hourspkcmd7bvr.onion'

                    net_type = 'tor'

                    spider_name = 'onion_hour24_market_spider'

                    try:
                        goods_name = response.xpath('//h1/text()')[0].strip()
                    except:
                        goods_name = ''

                    try:
                        goods_id = record["_source"]["url"]
                        goods_id = re.findall('http://24hourspkcmd7bvr.onion/product/(.*?).html', goods_id)[0]
                    except:
                        goods_id = ''

                    url = record["_source"]["url"]

                    try:
                        description = response.xpath('//div[@class="product_desc2"]//text()')
                        goods_info = ''
                        for i in description:
                            goods_info += i
                    except:
                        goods_info = ''

                    try:
                        goods_img_url = []
                        img_url = response.xpath('//div[@class="item"]/div[@class="fltlft"]/img/@src')[0]  # 图片
                        img_url = 'http://24hourspkcmd7bvr.onion' + str(img_url)
                        goods_img_url.append(img_url)
                    except:
                        goods_img_url = []

                    try:
                        crawl_category = response.xpath(
                            '//table[@class="product_options"]/tr[5]/td[2]/text()|//table[@class="product_options"]/tr[6]/td[2]/text()')[
                            0]
                    except:
                        crawl_category = ''

                    try:
                        pros_count = response.xpath('//div[@class="item"]/ul/li[2]/a/text()')[0]
                        sold_count = re.findall(r'\d', pros_count)[0]
                        sold_count = int(sold_count)
                    except:
                        sold_count = None

                    try:
                        price = response.xpath(
                            '//tr[@class="odd"]/td/p[2]/span/text()|//tr[@class="odd"]/td/p[3]/span/text()|//tr[@class="even"]/td/p[3]/span/text()')
                    except:
                        price = []

                    try:
                        user_id = re.findall(r'Company:</b></td><td>(.*?)</td>', html)[0].strip()
                        if user_id == '':
                            user_id = '24hour'
                    except:
                        user_id = '24hour'


                    try:
                        user_name = re.findall(r'Company:</b></td><td>(.*?)</td>', html)[0].strip()
                        if user_name == '':
                            user_name = '24hour'
                    except:
                        user_name = '24hour'


                    try:
                        goods_areas = re.findall(r'Company:</b></td><td>(.*?)</td>', html)[0]
                        goods_area = goods_areas.split(' ')
                        goods_area = goods_area[-1].replace('(', '').replace(')', '')
                    except:
                        goods_area = ''

                    raw_publish_time = ''
                    publish_time = record["_source"]["crawl_time"]
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
                            # "raw_publish_time":raw_publish_time,
                            "publish_time": publish_time,
                            "sku": sku,
                            "bitcoin_addresses": bitcoin_addresses,
                            "eth_addresses": eth_addresses,
                            "gmt_create": record["_source"]["gmt_create"],
                            "gmt_modified": record["_source"]["gmt_modified"],
                        }
                    }]
                    success, _ = bulk(es, actions, index='goods', raise_on_exception=False, raise_on_error=False)
            except Exception as e:
                logger.warning(e)

if __name__ == '__main__':
    a = Analysis()
    a.exquisite()