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
                        "query": "nytimes3xbfgragh.onion"
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
            response = etree.HTML(html.encode('utf-8'))
            try:
                # user
                if record["_source"]["url"][0:37] == 'https://www.nytimes3xbfgragh.onion/20':
                    spider_name = 'onion_nytime_new_spider'

                    domain = 'nytimes3xbfgragh.onion'

                    net_type = 'tor'

                    if len(response.xpath('//p[@itemprop="author"]//span')) > 0:
                        user_name = response.xpath('//p[@itemprop="author"]//span/text()')
                        user_name = ' '.join(user_name)
                    else:
                        user_name = 'NyTimes'

                    user_description = ''

                    if len(response.xpath('//p[@itemprop="author"]//span')) > 0:
                        user_id = response.xpath('//p[@itemprop="author"]//span/text()')
                        user_id = ' '.join(user_id)
                    else:
                        user_id = 'NyTimes'

                    url = record["_source"]["url"]
                    raw_register_time = ''
                    register_time = None
                    user_img_url = ''

                    emails = email_extract(user_description)

                    bitcoin_addresses = bitcoin_extract(user_description)

                    eth_addresses = eth_extract(user_description)

                    try:
                        raw_last_active_time = response.xpath('//time/@datetime')[0].strip().replace('-05:00','').replace('-04:00', '')
                    except:
                        raw_last_active_time = ''

                    try:
                        last_active_time = datetime.strptime(raw_last_active_time, '%Y-%m-%dT%H:%M:%S')
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

                # topic
                if record["_source"]["url"][0:37] == 'https://www.nytimes3xbfgragh.onion/20':

                    spider_name = 'onion_nytime_new_spider'

                    domain = 'nytimes3xbfgragh.onion'

                    url = record["_source"]["url"]

                    page_index_id = record["_id"]

                    net_type = 'tor'

                    topic_type = 'news'

                    try:
                        crawl_tags = response.xpath('//span[@class="css-17xtcya"]/a/text()')
                    except:
                        crawl_tags = []

                    try:
                        titles = response.xpath('//span[@class="css-fwqvlz"]/text()')
                        title = ''
                        for i in titles:
                            title += i
                    except:
                        title = ''

                    try:
                        topic_id = record["_source"]["url"]
                        if topic_id.split('/')[-1] == '':
                            topic_id = topic_id.split('/')[-2]
                            print(topic_id)
                        else:
                            topic_id = topic_id.split('/')[-1].replace('.html', '')
                            print(topic_id)
                    except:
                        topic_id = ''

                    if len(response.xpath('//p[@itemprop="author"]//span')) > 0:
                        user_id = response.xpath('//p[@itemprop="author"]//span/text()')
                        user_id = ' '.join(user_id)
                    else:
                        user_id = 'NyTimes'

                    if len(response.xpath('//p[@itemprop="author"]//span')) > 0:
                        user_name = response.xpath('//p[@itemprop="author"]//span/text()')
                        user_name = ' '.join(user_name)
                    else:
                        user_name = 'NyTimes'

                    commented_user_id = ''
                    comment_id = ''

                    try:
                        raw_content = response.xpath('//main[@id="site-content"]')[0]
                        raw_content = etree.tostring(raw_content, encoding='utf-8')
                        raw_content = str(raw_content, encoding='utf-8')
                    except:
                        raw_content = ''

                    try:
                        contents = response.xpath('//div[@class="site-content"]')
                        content = contents[0].xpath('string(.)')
                    except:
                        content = ''

                    clicks_times = None
                    commented_times = None
                    crawl_time = record["_source"]["crawl_time"]

                    try:
                        raw_publish_time = response.xpath('//time/@datetime')[0].strip().replace('-05:00', '').replace('-04:00', '')
                    except:
                        raw = re.findall('onion/(.*?)/(.*?)/(.*?)/',url)[0]
                        raw_publish_time = ''
                        for i in raw:
                            raw_publish_time += i + ' '

                    try:
                        publish_time = datetime.strptime(raw_publish_time, '%Y %m %d ')
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
                            #"commented_user_id": commented_user_id,
                            #"comment_id": comment_id,
                            "raw_content": raw_content,
                            "content": content,
                            #"clicks_times": clicks_times,
                            #"commented_times": commented_times,
                            "crawl_time": crawl_time,
                            "publish_time": publish_time,
                            "raw_publish_time": raw_publish_time,
                            #"thumbs_up": thumbs_up,
                            #"thumbs_down": thumbs_down,
                            "emails": emails,
                            "bitcoin_addresses": bitcoin_addresses,
                            "eth_addresses": eth_addresses,
                            "gmt_create": record["_source"]["gmt_create"],
                            "gmt_modified": record["_source"]["gmt_modified"],
                        }
                    }]
                    success, _ = bulk(es, actions, index='topic', raise_on_exception=False, raise_on_error=False)

                # user
                if record["_source"]["url"][0:33] == 'https://cn.nytimes3xbfgragh.onion' and '20' in record["_source"][
                    "url"] and "topic" not in record["_source"]["url"] and len(response.xpath('//main[@class="container-fluid main clearfix"]/div')) > 1:
                    spider_name = 'onion_nytime_new_spider'

                    domain = 'nytimes3xbfgragh.onion'

                    net_type = 'tor'

                    if len(response.xpath('//div[@class="byline"]/address')) > 0:
                        user_name = response.xpath('//div[@class="byline"]/address/text()')
                        user_name = ' '.join(user_name)
                    else:
                        user_name = response.xpath('//meta[@name="apple-mobile-web-app-title"]/@content')[0]

                    user_description = ''

                    if len(response.xpath('//div[@class="byline"]/address')) > 0:
                        user_id = response.xpath('//div[@class="byline"]/address/text()')
                        user_id = ' '.join(user_id)
                    else:
                        user_id = response.xpath('//meta[@name="apple-mobile-web-app-title"]/@content')[0]

                    url = record["_source"]["url"]
                    raw_register_time = ''
                    register_time = None
                    user_img_url = ''

                    emails = email_extract(user_description)

                    bitcoin_addresses = bitcoin_extract(user_description)

                    eth_addresses = eth_extract(user_description)

                    try:
                        raw_last_active_time = response.xpath('//div[@class="byline"]/time/@datetime')[0].strip()
                    except:
                        raw_last_active_time = ''

                    try:
                        last_active_time = datetime.strptime(raw_last_active_time, '%Y-%m-%d %H:%M:%S')
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

                # topic
                if record["_source"]["url"][0:33] == 'https://cn.nytimes3xbfgragh.onion' and '20' in record["_source"][
                    "url"] and "topic" not in record["_source"]["url"] and len(response.xpath('//main[@class="container-fluid main clearfix"]/div')) > 1:

                    spider_name = 'onion_nytime_new_spider'

                    domain = 'nytimes3xbfgragh.onion'

                    url = record["_source"]["url"]

                    page_index_id = record["_id"]

                    net_type = 'tor'

                    topic_type = 'news'

                    try:
                        crawl_tags = response.xpath('//div[@class="col-4 section-title"]/h3/text()')
                    except:
                        crawl_tags = []

                    try:
                        title = response.xpath('//h1/text()')[0]
                    except:
                        title = ''

                    try:
                        topic_id = record["_source"]["url"]
                        if topic_id.split('/')[-1] == '':
                            topic_id = topic_id.split('/')[-2]
                            print(topic_id)
                        else:
                            topic_id = topic_id.split('/')[-1].replace('.html', '')
                            print(topic_id)
                    except:
                        topic_id = ''

                    if len(response.xpath('//div[@class="byline"]/address')) > 0:
                        user_id = response.xpath('//div[@class="byline"]/address/text()')
                        user_id = ' '.join(user_id)
                    else:
                        user_id = response.xpath('//meta[@name="apple-mobile-web-app-title"]/@content')[0]

                    if len(response.xpath('//div[@class="byline"]/address')) > 0:
                        user_name = response.xpath('//div[@class="byline"]/address/text()')
                        user_name = ' '.join(user_name)
                    else:
                        user_name = response.xpath('//meta[@name="apple-mobile-web-app-title"]/@content')[0]

                    commented_user_id = ''
                    comment_id = ''

                    try:
                        raw_content = response.xpath('//div[@class="article-left"]')[0]
                        raw_content = etree.tostring(raw_content, encoding='utf-8')
                        raw_content = str(raw_content, encoding='utf-8')
                    except:
                        raw_content = ''

                    try:
                        contents = response.xpath('//div[@class="article-left"][1]')
                        content = contents[0].xpath('string(.)')
                    except:
                        content = ''

                    clicks_times = None
                    commented_times = None
                    crawl_time = record["_source"]["crawl_time"]

                    try:
                        raw_publish_time = response.xpath('//div[@class="byline"]/time/@datetime')[0].strip()
                    except:
                        raw_publish_time = response.xpath('//meta[@id="date"]/@content')[0].replace('.000Z','')

                    try:
                        publish_time = datetime.strptime(raw_publish_time, '%Y-%m-%d %H:%M:%S')
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
                            #"commented_user_id": commented_user_id,
                            #"comment_id": comment_id,
                            "raw_content": raw_content,
                            "content": content,
                            #"clicks_times": clicks_times,
                            #"commented_times": commented_times,
                            "crawl_time": crawl_time,
                            "publish_time": publish_time,
                            "raw_publish_time": raw_publish_time,
                            #"thumbs_up": thumbs_up,
                            #"thumbs_down": thumbs_down,
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
