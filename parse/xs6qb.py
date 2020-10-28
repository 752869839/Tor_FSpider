# -*- coding: utf-8 -*-
import time
import re
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta
from elasticsearch6.helpers import bulk,scan
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
                        "query": "xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion"
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
            soup = BeautifulSoup(html, 'lxml')
            try:
                # user
                if record["_source"]["url"][
                   0:87] == 'http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion/viewtopic.php?tid':

                    spider_name = 'onion_xs6qb_market_spider'

                    domain = 'xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion'

                    net_type = 'tor'

                    try:
                        user_name = response.xpath('//table[@class="v_table_1"]//tr[5]/td[2]/text()')[0].strip()
                    except:
                        user_name = response.xpath('//div[@class="div_postboxa"]/font/text()')[0].strip()

                    user_description = ''

                    try:
                        user_id = response.xpath('//table[@class="v_table_1"]//tr[5]/td[2]/text()')[0].strip()
                    except:
                        user_id = response.xpath('//div[@class="div_postboxa"]/font/text()')[0].strip()

                    url = record["_source"]["url"]
                    raw_register_time = ''
                    register_time = None
                    user_img_url = ''

                    try:
                        user = response.xpath('//div[@class="vendorbio-description"]/p[6]/text()')
                        user_description = ''
                        for i in user:
                            user_description += i + '\n'

                        email = re.findall(r'email.(.*?)com', user_description)[0]
                        s = email + 'com'
                        emails = []
                        emails.append(s)
                    except:
                        emails = []

                    # emails = email_extract(user_description)

                    bitcoin_addresses = bitcoin_extract(user_description)

                    eth_addresses = eth_extract(user_description)

                    try:
                        raw_last_active_time = response.xpath('//table[@class="v_table_1"]//tr[5]/td[6]/text()')[
                            0].strip()
                    except:
                        raw_last_active_time = ''

                    try:
                        last_active_time = datetime.strptime(raw_last_active_time, '%Y-%m-%d %H:%M')
                        last_active_time = last_active_time - relativedelta(hours=8)
                    except:
                        last_active_time = None

                    area = ''
                    ratings = ''
                    level = ''
                    member_degree = ''
                    pgp = ''

                    crawl_time = record["_source"]["crawl_time"]
                    topic_nums = None
                    goods_orders = None
                    identity_tags = 'seller'

                    id = sim_hash.u_id(spider_name, user_id)
                    actions = [{
                        "_index": 'user',
                        "_type": '_doc',
                        "_op_type": 'create',
                        '_id': id,
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
                            "last_active_time": last_active_time,
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
                if record["_source"]["url"][
                   0:87] == 'http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion/viewtopic.php?tid':

                    crawl_time = record["_source"]["crawl_time"]

                    domain = 'xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion'

                    net_type = 'tor'

                    spider_name = 'onion_xs6qb_market_spider'

                    try:
                        goods_name = response.xpath('//a[@class="link_blue"][3]/text()')[0].strip()
                    except:
                        goods_name = ''

                    try:
                        goods_id = record["_source"]["url"]
                        goods_id = re.findall(r'tid=([\s|\S]+)', goods_id)[0]
                    except:
                        goods_id = ''

                    url = record["_source"]["url"]

                    try:
                        metas = response.xpath('//div[@class="div_masterbox"]/t/text()')
                        goods_info = ''
                        for i in metas:
                            goods_info += i + '\n'
                    except:
                        goods_info = ''

                    try:
                        goods_img_url = response.xpath('//img[@class="attach_image"]/@src')
                    except:
                        goods_img_url = []

                    try:
                        crawl_category = response.xpath('//a[@class="link_blue"][2]/text()')[0].strip()
                    except:
                        crawl_category = ''

                    try:
                        # sold_count = response.xpath('//table[@class="v_table_1"]//text()')[-1].strip()
                        # sold_count = int(sold_count)
                        sold_count = soup.select('.v_table_1 > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(4)')[0].get_text()
                    except:
                        sold_count = None

                    try:
                        price = []
                        p = response.xpath('//table[@class="v_table_1"]//tr[3]/td[4]//text()')[0].strip()
                        prices = p + '$'
                        price.append(prices)
                    except:
                        price = []

                    try:
                        user_id = response.xpath('//table[@class="v_table_1"]//tr[5]/td[2]/text()')[0].strip()
                    except:
                        user_id = response.xpath('//div[@class="div_postboxa"]/font/text()')[0].strip()

                    try:
                        user_name = response.xpath('//table[@class="v_table_1"]//tr[5]/td[2]/text()')[0].strip()
                    except:
                        user_name = response.xpath('//div[@class="div_postboxa"]/font/text()')[0].strip()

                    goods_area = ''

                    try:
                        raw_publish_time = response.xpath('//table[@class="v_table_1"]//tr[3]/td[6]/text()')[0].strip()
                    except:
                        raw_publish_time = response.xpath('//div[@class="div_postboxa"]/text()')[1].strip()
                        raw_publish_time = re.findall(r'时间: ([\s|\S]+)', raw_publish_time)[0]

                    try:
                        publish_time = datetime.strptime(raw_publish_time, '%Y-%m-%d %H:%M')
                        publish_time = publish_time - relativedelta(hours=8)
                    except:
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
            except Exception as e:
                logger.warning(e)

if __name__ == '__main__':
    a = Analysis()
    a.exquisite()