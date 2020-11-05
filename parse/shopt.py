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
                        "query": "shoptwgap2x3xbwy.onion"
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
                if record["_source"]["url"][0:41] == 'http://shoptwgap2x3xbwy.onion/shop/detail':

                    crawl_time = record["_source"]["crawl_time"]

                    domain = 'shoptwgap2x3xbwy.onion'

                    net_type = 'tor'

                    spider_name = 'onion_shopt_market_spider'

                    try:
                        goods_name = response.xpath('//h1[@class="product_title entry-title"]/text()')[0].strip()
                    except:
                        goods_name = ''

                    try:
                        goods_id = response.xpath('//h1[@class="product_title entry-title"]/text()')[0].strip()
                    except:
                        goods_id = ''

                    url = record["_source"]["url"]

                    try:
                        goods_info = ''
                        info = response.xpath('//div[@id="tab-description"]//text()')
                        for i in info:
                            goods_info += i + '\n'
                    except:
                        goods_info = ''

                    try:
                        goods_img_url = response.xpath('//img[@class="wp-post-image"]/@src')  # 图片
                    except:
                        goods_img_url = []

                    try:
                        crawl_category = response.xpath('//nav[@class="woocommerce-breadcrumb"]/a[3]/text()')[0].strip()
                    except:
                        crawl_category = ''

                    try:
                        sold_count = response.xpath('//div[@class="summary entry-summary"]/p/text()')[0]
                        sold_count = re.findall('已销售: (\d+)', sold_count)[0]
                        sold_count = int(sold_count)
                    except:
                        sold_count = None

                    try:
                        price = response.xpath('//p[@class="price"]/span/text()')
                        price = [i + "$" for i in price]
                    except:
                        price = []

                    try:
                        user_id = response.xpath('//div[@id="tab-yith_wc_vendor"]/h2/a/text()')[0].strip()
                    except:
                        user_id = ''

                    try:
                        user_name = response.xpath('//div[@id="tab-yith_wc_vendor"]/h2/a/text()')[0].strip()
                    except:
                        user_name = ''

                    goods_area = ''
                    raw_publish_time = ''
                    publish_time = None

                    try:
                        sku = response.xpath('//span[@class="sku_wrapper"]/span/text()')[0]
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