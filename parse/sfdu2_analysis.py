# -*- coding: utf-8 -*-
import re
import time
from lxml import etree
from elasticsearch6.helpers import bulk, scan
from datetime import datetime
from dateutil.relativedelta import relativedelta
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
                        "query": "sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion"
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
                if record["_source"]["url"][0:80] == 'http://sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion/goods/info':

                    crawl_time = record["_source"]["crawl_time"]

                    domain = 'sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion'

                    net_type = 'tor'

                    spider_name = 'onion_sfdu2_market_spider'

                    try:
                        goods_name = response.xpath('//h3/text()')[0].strip()
                    except:
                        goods_name = ''

                    try:
                        goods_id = record["_source"]["url"]
                        goods_id = re.findall('id=(\d+)', goods_id)[0]
                    except:
                        goods_id = ''

                    url = record["_source"]["url"]

                    try:
                        goods_info = ''
                        info = response.xpath('//div[@id="tab_one"][2]//text()')
                        for i in info:
                            goods_info += i.strip()
                    except:
                        goods_info = ''

                    try:
                        goods_img_url = response.xpath('//img[@alt="封面"]/@src')  # 图片
                        goods_img_url = ['http://sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion' + i for i in goods_img_url]
                    except:
                        goods_img_url = []

                    crawl_category = ''

                    try:
                        sold_count = response.xpath('//div[@class="pro-review"]/span/a/text()')[0]
                        sold_count = re.findall('销售量 (\d+)', sold_count)[0]
                        sold_count = int(sold_count)
                    except:
                        sold_count = None

                    try:
                        price = response.xpath('//span[@class="regular-price"]/text()')
                    except:
                        price = []

                    try:
                        user_id = response.xpath('//div[@id="tab_one"]/p[2]/span/text()')[0].strip()
                    except:
                        user_id = ''

                    try:
                        user_name = response.xpath('//div[@id="tab_one"]/p[2]/span/text()')[0].strip()
                    except:
                        user_name = ''

                    goods_area = ''

                    try:
                        raw_publish_time = response.xpath('//div[@id="tab_one"]/p[last()]/span/text()')[0]
                    except:
                        raw_publish_time = ''

                    try:
                        publish_time = datetime.strptime(raw_publish_time, '%Y-%m-%d %H:%M:%S')
                        publish_time = publish_time - relativedelta(hours=8)
                    except:
                        publish_time = None

                    try:
                        sku = response.xpath('//div[@class="availability mb-20"]/span/text()')[0]
                    except:
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