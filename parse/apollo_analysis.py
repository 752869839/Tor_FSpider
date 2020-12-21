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
from log_decorator import _logger, exception_logger

logger = _logger()

class Analysis(object):
    def exquisite(self):
        search_query = {
            "query": {
                "match_phrase": {
                    "domain": {
                        "query": "apollonvm7uin7yw.onion"
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
                # user
                if record["_source"]["url"][0:38] == 'http://apollonvm7uin7yw.onion/user.php' and '&' not in record["_source"]["url"]:

                    spider_name = 'onion_apollo_market_spider'

                    domain = 'apollonvm7uin7yw.onion'

                    net_type = 'tor'

                    try:
                        user_name = response.xpath('//div[@class="col-sm-5"]/small/a/b/text()')[0]
                        user_name = re.findall(r'[a-zA-Z]+', user_name)[0]
                    except:
                        user_name = response.xpath('//div[@class="col-sm-5"]/small/a/b/text()')[0]
                        user_name = re.findall(r'.*? ', user_name)[0].strip()

                    try:
                        user_descriptions = response.xpath('//div[@class="col-lg-13"]//text()')
                        user_description = ''
                        for i in user_descriptions:
                            user_description += i.strip() + '\n'
                    except:
                        user_description = ''

                    try:
                        user_id = record["_source"]["url"]
                        user_id = re.findall(r'id=([\s|\S]+)', user_id)[0]
                    except:
                        user_id = ''

                    try:
                        url = record["_source"]["url"]
                    except:
                        url = ''

                    try:
                        raw_register_time = response.xpath('//div[@class="col-sm-5"][1]/small[5]/span/text()')[
                            0].strip().replace(',', '')
                    except:
                        raw_register_time = ''

                    try:
                        register_time = datetime.strptime(raw_register_time, '%b %d %Y')
                        register_time = register_time - relativedelta(hours=8)
                    except:
                        register_time = None

                    try:
                        user_img_url = response.xpath('//img[@class="img-responsive img-rounded"]/@src')[0]
                        user_img_url = 'http://apollonvm7uin7yw.onion/' + user_img_url
                    except:
                        user_img_url = ''


                    emails = email_extract(user_description)

                    bitcoin_addresses = bitcoin_extract(user_description)

                    eth_addresses = eth_extract(user_description)

                    try:
                        raw_last_active_time = response.xpath('//div[@class="col-sm-5"][1]/small[6]/span/text()')[
                            0].replace(',', '')
                    except:
                        raw_last_active_time = ''

                    try:
                        last_active_time = datetime.strptime(raw_last_active_time, '%b %d %Y')
                        last_active_time = last_active_time - relativedelta(hours=8)
                    except:
                        last_active_time = None

                    area = ''

                    try:
                        ratings = response.xpath('//div[@class="col-sm-5"][1]/small[1]/small[2]/span/text()')[0].strip().replace('Trust Level ','').replace(' (0K)','')
                    except:
                        ratings = ''

                    try:
                        level = response.xpath('//div[@class="col-sm-5"][1]/small[1]/small[1]/span/text()')[0]
                        level = re.findall(r'Seller Level([\s|\S]+)', level)[0].split(' ')[1]
                    except:
                        level = ''


                    member_degree = ''

                    try:
                        pgp = response.xpath('//div[@class="col-sm-5"][2]/pre/text()')[0].strip()
                    except:
                        pgp = ''


                    try:
                        crawl_time = record["_source"]["crawl_time"]
                    except:
                        crawl_time = ''

                    topic_nums = None

                    try:
                        goods_orders = response.xpath('//div[@class="col-sm-2"]/small[2]/span/text()')[0]
                        goods_orders = int(goods_orders)
                    except:
                        goods_orders = None

                    identity_tags = 'seller'

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
                            "register_time": register_time,
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
                            # "topic_nums": topic_nums,
                            "goods_orders": goods_orders,
                            "identity_tags": identity_tags,
                            "gmt_create": record["_source"]["gmt_create"],
                            "gmt_modified": record["_source"]["gmt_modified"],
                        }
                    }]
                    success, _ = bulk(es, actions, index='user', raise_on_exception=False, raise_on_error=False)


                # goods
                if record["_source"]["url"][0:41] == 'http://apollonvm7uin7yw.onion/listing.php':

                    crawl_time = record["_source"]["crawl_time"]

                    domain = 'apollonvm7uin7yw.onion'

                    net_type = 'tor'

                    spider_name = 'onion_apollo_market_spider'

                    try:
                        goods_name = response.xpath('//div[@class="col-sm-12"][1]/a/text()')[0].strip()
                    except:
                        goods_name = ''

                    try:
                        goods_id = record["_source"]["url"]
                        goods_id = re.findall(r'id=([\s|\S]+)', goods_id)[0]
                    except:
                        goods_id = ''

                    url = record["_source"]["url"]

                    try:
                        goods_info = response.xpath('//pre[last()]/text()')[0].strip() + '\n'
                    except:
                        goods_info = ''

                    try:
                        goods_img_url = []
                        img_url = response.xpath('//img[@class="img-responsive inline-block img-rounded"]/@src')[0]  # 图片
                        img_url = 'http://apollonvm7uin7yw.onion/' + img_url
                        goods_img_url.append(img_url)
                    except:
                        goods_img_url = []

                    try:
                        crawl_category = response.xpath('//div[@class="col-sm-12"]/div[3]/small[last()-1]/text()')[0].strip()
                    except:
                        crawl_category = ''

                    try:
                        sold_count = response.xpath('//div[@class="col-sm-12"]/div[2]/small[7]/span/text()')[0]
                        sold_count = int(sold_count)
                    except:
                        sold_count = None

                    try:
                        prices = response.xpath('//span[@class="label label-info"]//text()')
                        prices_len = len(prices)

                        price = []
                        for i in range(0, prices_len, 4):
                            slice = prices[i:i + 4]
                            m1 = re.search("[0-9.]+", slice[0])
                            price1 = 0
                            if m1:
                                price1 = m1.group(0)
                            unit1 = slice[1]
                            price2 = slice[2].replace("/", '').strip()
                            unit2 = slice[3]
                            result1 = price1 + unit1
                            result2 = price2 + unit2
                            if not result1 in price:
                                price.append(result1 + '/' + result2)
                    except:
                        price = []

                    try:
                        user_id = response.xpath('//div[@class="col-sm-3"][2]/small[1]/a/@href')[0]
                        user_id = re.findall(r'id=([\s|\S]+)', user_id)[0]
                    except:
                        user_id = ''

                    try:
                        user_name = response.xpath('//div[@class="col-sm-3"][2]/small[1]/a/@href')[0]
                        user_name = re.findall(r'id=([\s|\S]+)', user_name)[0]
                    except:
                        user_name = ''

                    try:
                        goods_area = response.xpath('//div[@class="col-sm-12"]/div[3]/small[2]/text()')[0].strip()
                    except:
                        goods_area = ''

                    raw_publish_time = ''
                    publish_time = record["_source"]["crawl_time"]
                    try:
                        sku = response.xpath('//div[@class="col-sm-12"]/div[3]/small[last()]/text()')[
                            0].strip().replace(' Available', '')
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

    def update(self):
        search_query = {
            "query": {
                "match_phrase": {
                    "domain": {
                        "query": "apollonvm7uin7yw.onion"
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

            if record["_source"]["url"][0:42] == 'http://apollonvm7uin7yw.onion/home.php?cid':
                try:
                    urls = response.xpath('//div[@class="col-sm-8"]/small[1]/a/@href|//div[@class="col-sm-8"]/small/i/text()')
                    urls = [x for x in urls]
                    data = []
                    index_url = 'http://apollonvm7uin7yw.onion/'
                    for index in range(0, len(urls), 2):
                        if index > 0:
                            list_info = urls[index - 2:index]
                            list_info[0] = index_url + list_info[0]
                            # print(list_info)
                            data.append(list_info)

                    for j in range(1, len(data)):
                        url = data[j][0]

                        raw_publish_time = data[j][1]
                        raw_publish_time = raw_publish_time.replace(',', '')

                        publish = datetime.strptime(raw_publish_time, '%b %d %Y')
                        publish_time = publish - relativedelta(hours=8)

                        goods_id = re.findall(r'id=([\s|\S]+)', url)[0]
                        print('goods_id:',goods_id)

                        search_query = {
                            "query": {
                                "bool": {
                                    "must": [
                                        {"match": {
                                            "domain": "apollonvm7uin7yw.onion"}},
                                        {"match": {
                                            "goods_id": goods_id}}
                                    ]
                                }
                            }
                        }
                        r = es.search(index='goods', doc_type='_doc', body=search_query, timeout='500m')
                        res_lst = r["hits"]["hits"]
                        for rec in res_lst:
                            if goods_id in rec["_source"]["url"]:
                                _id = rec["_id"]
                                insert_body = {
                                    "script": {
                                        "source": "ctx._source.raw_publish_time=params.raw_publish_time ; ctx._source.publish_time=params.publish_time ; ctx._source.gmt_modified=params.gmt_modified",
                                        "params": {
                                            "raw_publish_time": raw_publish_time,
                                            "publish_time": publish_time,
                                            "gmt_modified": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
                                        }
                                    }
                                }
                                es.update(index="goods", doc_type="_doc", id=_id, body=insert_body)
                except Exception as e:
                    logger.warning(e)

            if record["_source"]["url"][0:38] == 'http://apollonvm7uin7yw.onion/user.php' and '&' in record["_source"]["url"]:
                try:
                    pgps = response.xpath('//div[@class="col-sm-5"]/pre/text()')
                    pgps = [x for x in pgps]

                    for j in pgps:
                        pgp = j
                        print(pgp)
                        user_id = re.findall('id=(.*?)&',record["_source"]["url"])[0]
                        print('user_id:',user_id)

                        search_query = {
                            "query": {
                                "bool": {
                                    "must": [
                                        {"match": {
                                            "domain": "apollonvm7uin7yw.onion"}},
                                        {"match": {
                                            "user_id": user_id}}
                                    ]
                                }
                            }
                        }
                        r = es.search(index='user', doc_type='_doc', body=search_query, timeout='5m')
                        cnt = 0
                        res_lst = r["hits"]["hits"]
                        for rec in res_lst:
                            if user_id in rec["_source"]["url"]:
                                _id = rec["_id"]
                                insert_body = {
                                    "script": {
                                        "source": "ctx._source.pgp=params.pgp ; ctx._source.gmt_modified=params.gmt_modified",
                                        "params": {
                                            "pgp": pgp,
                                            "gmt_modified": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
                                        }
                                    }
                                }
                                es.update(index="user", doc_type="_doc", id=_id, body=insert_body)
                except Exception as e:
                    logger.warning(e)


if __name__ == '__main__':
    a = Analysis()
    a.exquisite()
    a.update()