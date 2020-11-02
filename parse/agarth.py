# -*- coding: utf-8 -*-
import re
import time
from lxml import etree
from datetime import datetime,timedelta
from elasticsearch6.helpers import bulk,scan
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
                        "query": "agarthaangodtcz3.onion"
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
                if record["_source"]["url"][0:36] == 'http://agarthaangodtcz3.onion/vendor':

                    spider_name = 'onion_agarth_market_spider'

                    domain = 'agarthaangodtcz3.onion'

                    net_type = 'tor'

                    try:
                        user_name = response.xpath('//div[@id="middlestuff"]/div[1]/strong/text()')[0].strip()
                    except:
                        user_name = ''

                    try:
                        user = response.xpath('//div[@class="vendorbio-description"]/p[5]/text()')
                        user_description = ''
                        for i in user:
                            user_description += i + '\n'
                    except:
                        user_description = ''

                    try:
                        user_id = record["_source"]["url"]
                        user_id = re.findall(r'vendor/([\s|\S]+)', user_id)[0]
                    except:
                        user_id = ''

                    url = record["_source"]["url"]

                    try:
                        raw_register_time = response.xpath('//div[@class="vendorbio-stats-online"]/text()')[0].strip()
                    except:
                        raw_register_time = ''

                    if 'Months' in raw_register_time:
                        num = re.findall(r'Registered (.*?) Months', raw_register_time)[0]
                        num = int(num)
                        register_time = datetime.today() - relativedelta(months=+num)
                        register_time = register_time - relativedelta(hours=8)
                    elif 'Week' in raw_register_time:
                        num = re.findall(r'Registered (.*?) Week', raw_register_time)[0]
                        num = int(num)
                        register_time = datetime.today() - relativedelta(weeks=+num)
                        register_time = register_time - relativedelta(hours=8)
                    else:
                        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        register_time = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')

                    try:
                        user_img_url = response.xpath('//img[@id="avatar"]/@src')[0]
                        user_img_url = 'http://agarthaangodtcz3.onion' + user_img_url
                    except:
                        user_img_url = ''

                    emails = email_extract(user_description)

                    bitcoin_addresses = bitcoin_extract(user_description)

                    eth_addresses = eth_extract(user_description)


                    try:
                        raw_last_active_time = response.xpath('//div[@class="vendorbio-stats-online"]/text()')[
                            1].strip()
                    except:
                        raw_last_active_time = ''

                    if 'Today' in raw_last_active_time:
                        t = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                        last_active_time = datetime.strptime(t, '%Y-%m-%d')
                        last_active_time = last_active_time - relativedelta(hours=8)
                    elif 'Yesterday' in raw_last_active_time:
                        yesterday = datetime.today() + timedelta(-1)
                        yesterday_format = yesterday.strftime('%Y-%m-%d')
                        last_active_time = datetime.strptime(yesterday_format, '%Y-%m-%d')
                        last_active_time = last_active_time - relativedelta(hours=8)
                    else:
                        last_active_time = None

                    try:
                        area = response.xpath('//div[@class="vendorbio-description"]/p[4]/text()')[-1].strip()
                    except:
                        area = ''

                    try:
                        ratings = response.xpath('//div[@id="middlestuff"]/div[1]/span/text()')[-1].replace('(','').replace(')', '').strip()
                    except:
                        ratings = ''

                    try:
                        level = re.findall('Level: </b>(.*?)</p>', html)[0].strip()
                    except:
                        level = ''

                    member_degree = ''

                    try:
                        pgps = response.xpath('//div[@class="vendorbio-description"]/pre/text()')
                        pgp = ''
                        for i in pgps:
                            pgp += i + '\n'
                    except:
                        pgp = ''

                    try:
                        crawl_time = record["_source"]["crawl_time"]
                    except:
                        crawl_time = ''

                    topic_nums = None

                    try:
                        orders = response.xpath('//div[@class="vendorbio-stats-online"]/span/text()')
                        example = lambda x: x.replace('\n', '').replace('\t', '').strip()
                        orders1 = [example(x) for x in orders if example(x)]
                        data = re.findall('(\d+).-.(\d+)', orders1[0])[0]
                        goods_orders = '{} - {}'.format(data[0], data[1])
                        goods_orders = re.findall('\d+', goods_orders)[0]
                        goods_orders = int(goods_orders)
                    except:
                        goods_orders = None

                    identity_tags = 'seller'

                    id = sim_hash.u_id(spider_name, user_id)
                    actions = [{
                        "_index": 'user',
                        "_type": '_doc',
                        "_op_type" : 'create',
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
                            #"topic_nums": topic_nums,
                            "goods_orders": goods_orders,
                            "identity_tags": identity_tags,
                            "gmt_create": record["_source"]["gmt_create"],
                            "gmt_modified": record["_source"]["gmt_modified"],
                        }
                    }]
                    success, _ = bulk(es, actions, index='user', raise_on_exception=False, raise_on_error=False)


                # goods
                if record["_source"]["url"][0:34] == 'http://agarthaangodtcz3.onion/item':

                    crawl_time = record["_source"]["crawl_time"]

                    domain = 'agarthaangodtcz3.onion'

                    net_type = 'tor'

                    spider_name = 'onion_agarth_market_spider'

                    try:
                        goods_name = response.xpath('//div[@class="panel-heading"]/h2/text()')[0].strip()
                    except:
                        goods_name = ''

                    try:
                        goods_id = record["_source"]["url"]
                        goods_id = re.findall(r'item/([\s|\S]+)', goods_id)[0]
                    except:
                        goods_id = ''

                    try:
                        url = record["_source"]["url"]
                    except:
                        url = ''

                    try:
                        metas = response.xpath('//div[@class="panel-body"]/p[2]/text()')
                        goods_info = ''
                        for i in metas:
                            goods_info += i + '\n'
                    except:
                        goods_info = ''

                    try:
                        goods_img_url = []
                        img_url = response.xpath('//img[@id="item_view_img"]/@src')[0]
                        img_url = 'http://agarthaangodtcz3.onion' + str(img_url)
                        goods_img_url.append(img_url)
                    except:
                        goods_img_url = []

                    try:
                        crawl_category = response.xpath('//td[@class="mainpagedividertd"]/div[1]/p/b/text()')[0].strip()
                    except:
                        crawl_category = ''

                    sold_count = None

                    try:
                        p = ""
                        a = response.xpath('//div[@class="panel-body"]/p[3]//text()')
                        for i in a:
                            p += i.strip().replace('Price:', '').replace(' &rpar;', '')
                        price = p.replace('\xa0', '').replace(')', '').split('&lpar;')
                    except:
                        price = []

                    try:
                        user_id = response.xpath('//div[@class="panel-body"]/p[1]/a/text()')[0].strip()
                    except:
                        user_id = ''

                    try:
                        user_name = response.xpath('//div[@class="panel-body"]/p[1]/a/text()')[0].strip()
                    except:
                        user_name = ''

                    try:
                        goods_area = ''
                        g = response.xpath('//div[@class="panel-body"]/p[6]/text()')
                        for i in g:
                            goods_area += i.strip()
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
                            #"sold_count": sold_count,
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
