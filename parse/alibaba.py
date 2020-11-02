# -*- coding: utf-8 -*-
import time
import re
from lxml import etree
from elasticsearch6.helpers import bulk, scan
import sim_hash
from config import es
from bit_eth_ema import bitcoin_extract,eth_extract,email_extract
from log_decorator import _logger, exception_logger

logger = _logger()

class Analysis(object):
    def exquisite(self):
        search_query = {
            "query": {
                "match_phrase": {
                    "domain": {
                        "query": "alibaba2kw6qoh6o.onion"
                    }
                }
            }
        }

        res = scan(client=es, query=search_query, scroll='10m', index='page', doc_type='_doc', timeout='50m')
        cnt = 0
        for record in res:
            print(cnt, record["_source"]["url"])
            cnt += 1
            html = record["_source"]["raw_text"]
            response = etree.HTML(html)
            try:
                if record["_source"]["url"][0:41] == 'http://alibaba2kw6qoh6o.onion/shop/detail':

                    crawl_time = record["_source"]["crawl_time"]

                    domain = 'alibaba2kw6qoh6o.onion'

                    net_type = 'tor'

                    spider_name = 'onion_alibaba_market_spider'

                    try:
                        goods_name = response.xpath('//div[@class="col-md-9"]/p/b/text()')[0].strip()
                    except:
                        goods_name = ''

                    try:
                        goods_id = record["_source"]["url"]
                        goods_id = re.findall(r'detail/([\s|\S]+)', goods_id)[0]
                    except:
                        goods_id = ''

                    url = record["_source"]["url"]

                    try:
                        goods_info = ''
                        info = response.xpath('//div[@class="mb-5"]//text()')
                        for i in info:
                            goods_info += i + '\n'
                    except:
                        goods_info = ''

                    try:
                        index_url = 'http://alibaba2kw6qoh6o.onion'
                        img_url = response.xpath(
                            '//div[@class="prod d-flex align-items-center justify-content-center"]//img/@src')  # 图片
                        goods_img_url = [index_url + i for i in img_url]
                    except:
                        goods_img_url = []

                    try:
                        crawl_category = response.xpath('//span[@class="text-info"]/text()')[0].strip()
                    except:
                        crawl_category = ''

                    try:
                        sold_count = response.xpath('//span[@class="text-info"][last()]/text()')[0].strip()
                        sold_count = int(sold_count)
                    except:
                        sold_count = None

                    try:
                        price = response.xpath(
                            '//span[@class="text-success"]/text()|//span[@class="text-muted"][last()]/text()')
                        price.remove("销售")
                    except:
                        price = []

                    try:
                        user_id = response.xpath('//span[@class="text-dark"]/text()')[0].strip()
                    except:
                        user_id = ''

                    try:
                        user_name = response.xpath('//span[@class="text-dark"]/text()')[0].strip()
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

            except Exception as e:
                logger.warning(e)

if __name__ == '__main__':
    a = Analysis()
    a.exquisite()