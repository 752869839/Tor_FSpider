# -*- coding: utf-8 -*-
import re
import time
from lxml import etree
from datetime import datetime
from dateutil.relativedelta import relativedelta
from elasticsearch6.helpers import bulk,scan
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
                        "query": "avengersdutyk3xf.onion"
                    }
                }
            }
        }

        res = scan(client=es, query=search_query, scroll='50m', index='page', doc_type='_doc', timeout='50m')
        cnt = 0
        for record in res:
            print(cnt, record["_source"]["url"])
            cnt += 1
            html = record["_source"]["raw_text"]
            response = etree.HTML(html)
            try:
                # user
                if record["_source"]["url"][0:35] == 'http://avengersdutyk3xf.onion/user-':

                    spider_name = 'onion_avenger_bbs_spider'

                    domain = 'avengersdutyk3xf.onion'

                    net_type = 'tor'

                    try:
                        user_name = response.xpath('//span[@class="largetext"]/strong//text()')[0].strip()
                    except:
                        user_name = ''

                    user_description = ''

                    try:
                        user_id = record["_source"]["url"]
                        user_id = re.findall(r'user-(.*?).html', user_id)[0]
                    except:
                        user_id = ''

                    try:
                        url = record["_source"]["url"]
                    except:
                        url = ''

                    try:
                        user = response.xpath(
                            '//span[@class="smalltext"][1]/strong/text()|//span[@class="smalltext"][1]/text()')
                        info = ''
                        for i in user:
                            info += i.replace('\n', '').replace('\t', '')
                        raw_register_time = re.findall(r'Registration Date:(.*?)Date of', info)[0].strip()
                    except:
                        raw_register_time = ''

                    try:
                        register_time = datetime.strptime(raw_register_time, '%m-%d-%Y')
                        register_time = register_time - relativedelta(hours=8)
                    except:
                        register_time = None

                    try:
                        img = response.xpath('//table/tr/td/img/@src')
                        user_img_url = ''
                        for i in img:
                            user_img_url += i.strip()
                        user_img_url = 'http://avengersdutyk3xf.onion' + user_img_url
                    except:
                        user_img_url = ''

                    emails = email_extract(user_description)

                    bitcoin_addresses = bitcoin_extract(user_description)

                    eth_addresses = eth_extract(user_description)

                    try:
                        raw_last_active_time = response.xpath(
                            '//table[@class="tborder"]/tr[3]/td[2]/span/text()|//table[@class="tborder"]/tr[3]/td[2]/text()')[
                            0].strip()
                    except:
                        raw_last_active_time = ''

                    try:
                        last_active_time = datetime.strptime(raw_last_active_time, '%m-%d-%Y, %H:%M %p')
                        last_active_time = last_active_time - relativedelta(hours=8)
                    except:
                        last_active_time = None

                    area = ''

                    try:
                        ratings = response.xpath('//img[@src="images/star.png"]')
                        ratings = str(len(ratings))
                    except:
                        ratings = ''

                    try:
                        levels = response.xpath('//img[@src="images/star.png"]')
                        level = str(len(levels))
                    except:
                        level = ''

                    member_degree = ''

                    try:
                        pgps = response.xpath('//td[@class="trow1 scaleimages"]/text()')
                        pgp = ''
                        for i in pgps:
                            pgp += i
                    except:
                        pgp = ''

                    try:
                        crawl_time = record["_source"]["crawl_time"]
                    except:
                        crawl_time = ''

                    try:
                        topic_nums = response.xpath('//table[@class="tborder"]/tr[4]/td[2]/text()')[0]
                        topic_nums = re.findall('(.*?) ', topic_nums)[0]
                        topic_nums = int(topic_nums)
                    except:
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
                            "topic_nums": topic_nums,
                            #"goods_orders": goods_orders,
                            "identity_tags": identity_tags,
                            "gmt_create": record["_source"]["gmt_create"],
                            "gmt_modified": record["_source"]["gmt_modified"],
                        }
                    }]
                    success, _ = bulk(es, actions, index='user', raise_on_exception=False, raise_on_error=False)

                # topic
                if record["_source"]["url"][0:36] == 'http://avengersdutyk3xf.onion/thread' and len(response.xpath('//div[@id="posts"]/div')) > 1 and "This post has been deleted." not in html:

                    spider_name = 'onion_avenger_bbs_spider'

                    domain = 'avengersdutyk3xf.onion'

                    url = record["_source"]["url"]

                    try:
                        page_index_id = record["_id"]
                    except:
                        page_index_id = ''

                    net_type = 'tor'

                    topic_type = 'post'

                    try:
                        crawl_tags = response.xpath('//div[@class="navigation"]/a[2]/text()')
                    except:
                        crawl_tags = []

                    try:
                        title = response.xpath('//span[@class="active"]/text()')[0].strip()
                    except:
                        title = ''

                    try:
                        topic_id = record["_source"]["url"]
                        topic_id = re.findall(r'thread-(.*?)-page', topic_id)[0]
                    except:
                        topic_id = record["_source"]["url"]
                        topic_id = re.findall(r'thread-(.*?).html', topic_id)[0]

                    try:
                        user_id = response.xpath('//span[@class="largetext"][1]/a/@href')[0]
                        user_id = re.findall(r'user-(.*?).html', user_id)[0]
                    except:
                        user_id = response.xpath('//span[@class="largetext"][1]//text()')[0].strip()

                    try:
                        user_name = response.xpath('//span[@class="largetext"][1]//text()')[0].strip()
                    except:
                        user_name = ''

                    commented_user_id = ''
                    comment_id = ''

                    try:
                        raw_content = response.xpath('//div[@class="post_body scaleimages"]')[0]
                        raw_content = etree.tostring(raw_content, encoding='utf-8')
                        raw_content = str(raw_content, encoding='utf-8')
                    except:
                        raw_content = ''

                    try:
                        contents = response.xpath('//div[@class="post_body scaleimages"][1]')
                        content = contents[0].xpath('string(.)')
                    except:
                        content = ''

                    clicks_times = None
                    commented_times = None

                    crawl_time = record["_source"]["crawl_time"]

                    try:
                        raw_publish_time = response.xpath('//span[@class="post_date"][1]/text()')[0].replace(',', '')
                    except:
                        raw_publish_time = ''

                    try:
                        publish_time = datetime.strptime(raw_publish_time, '%m-%d-%Y %I:%M %p ')
                        publish_time = publish_time - relativedelta(hours=8)
                    except:
                        publish_time = None

                    try:
                        thumbs_ups = response.xpath('//span[@class="largetext"]')
                        thumbs_up = str(len(thumbs_ups))
                        thumbs_up = int(thumbs_up)
                    except:
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
                            "clicks_times": clicks_times,
                            "commented_times": commented_times,
                            "crawl_time": crawl_time,
                            "publish_time": publish_time,
                            "raw_publish_time": raw_publish_time,
                            "thumbs_up": thumbs_up,
                            #"thumbs_down": thumbs_down,
                            "emails": emails,
                            "bitcoin_addresses": bitcoin_addresses,
                            "eth_addresses": eth_addresses,
                            "gmt_create": record["_source"]["gmt_create"],
                            "gmt_modified": record["_source"]["gmt_modified"],
                        }
                    }]
                    success, _ = bulk(es, actions, index='topic', raise_on_exception=False, raise_on_error=False)


                    p = response.xpath('//div[@id="posts"]/div')
                    if len(p) > 1:
                        poster_list = response.xpath('//div[@id="posts"]/div')
                        poster_lenght = len(poster_list)
                        for index in range(1, poster_lenght):
                            poster = poster_list[index]

                            spider_name = 'onion_avenger_bbs_spider'

                            domain = 'avengersdutyk3xf.onion'

                            url = record["_source"]["url"]

                            page_index_id = record["_id"]

                            net_type = 'tor'

                            topic_type = 'comment'

                            try:
                                crawl_tags = response.xpath('//div[@class="navigation"]/a[2]/text()')
                            except:
                                crawl_tags = []

                            try:
                                title = response.xpath('//span[@class="active"]/text()')[0].strip()
                            except:
                                title = ''

                            try:
                                topic_id = record["_source"]["url"]
                                topic_id = re.findall(r'thread-(.*?)-page', topic_id)[0]
                            except:
                                topic_id = record["_source"]["url"]
                                topic_id = re.findall(r'thread-(.*?).html', topic_id)[0]

                            try:
                                user_ids = poster.xpath('div[1]/div[2]/strong/span//@href')[0].strip()
                                user_id = re.findall(r'user-(.*?).html', user_ids)[0]
                            except:
                                user_id = poster.xpath('div[1]/div/strong/span//text()')[0].strip()

                            try:
                                user_name = poster.xpath('div[1]/div[2]/strong/span//text()')[0].strip()
                            except:
                                user_name = poster.xpath('div[1]/div/strong/span//text()')[0].strip()

                            try:
                                commented_user_id = response.xpath('//span[@class="largetext"][1]/a/@href')[0]
                                commented_user_id = re.findall(r'user-(.*?).html', commented_user_id)[0]
                            except:
                                commented_user_id = ''

                            try:
                                comment_id = poster.xpath('@id')[0].strip().replace('post_', '')
                            except:
                                comment_id = ''

                            try:
                                raw_content = poster.xpath('div//div[@class="post_body scaleimages"]')[0]
                                raw_content = etree.tostring(raw_content, encoding='utf-8')
                                raw_content = str(raw_content, encoding='utf-8')
                            except:
                                raw_content = ''

                            try:
                                contents = poster.xpath('div//div[@class="post_body scaleimages"]')
                                content = contents[0].xpath('string(.)')
                            except:
                                content = ''

                            clicks_times = None
                            commented_times = None

                            crawl_time = record["_source"]["crawl_time"]

                            try:
                                raw_publish_time = poster.xpath('div//span[@class="post_date"]/text()')[0].replace(',', '')
                            except:
                                raw_publish_time = ''

                            try:
                                publish_time = datetime.strptime(raw_publish_time, '%m-%d-%Y %I:%M %p ')
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

    def update(self):
        search_query = {
            "query": {
                "match_phrase": {
                    "domain": {
                        "query": "avengersdutyk3xf.onion"
                    }
                }
            }
        }
        res = scan(client=es, query=search_query, scroll='10m', index='page', doc_type='_doc', timeout='5m')
        cnt = 0
        for record in res:
            cnt += 1
            html = record["_source"]["raw_text"]
            response = etree.HTML(html)
            if record["_source"]["url"][0:36] == 'http://avengersdutyk3xf.onion/forum-':
                try:
                    urlss = response.xpath(
                        '//tr[@class="inline_row"]/td[3]/div/span/span[1]/a[1]/@href|//tr[@class="inline_row"]/td[4]/a/text()|//tr[@class="inline_row"]/td[5]/text()')
                    urls = [i for i in urlss if i != '-']
                    data = []
                    index_url = 'http://avengersdutyk3xf.onion/'
                    for index in range(0, len(urls), 3):
                        if index > 0:
                            list_info = urls[index - 3:index]
                            list_info[0] = index_url + list_info[0]
                            data.append(list_info)
                    for j in range(0, len(data)):
                        url = data[j][0]

                        replies = data[j][1]

                        views = data[j][2]
                        views = views.replace(',','')

                        topic_id = re.findall(r'thread-(.*?).html', url)[0]
                        print('topic_id:',topic_id)

                        search_query = {
                            "query": {
                                "bool": {
                                    "must": [
                                        {"match": {
                                            "domain": "avengersdutyk3xf.onion"}},
                                        {"match": {
                                            "topic_id": topic_id}}
                                    ]
                                }
                            }
                        }
                        r = es.search(index='topic', doc_type='_doc', body=search_query, timeout='5m')
                        cnt = 0
                        res_lst = r["hits"]["hits"]
                        for rec in res_lst:
                            if topic_id in rec["_source"]["url"]:
                                _id = rec["_id"]
                                insert_body = {
                                    "script": {
                                        "source": "ctx._source.clicks_times=params.clicks_times ; ctx._source.commented_times=params.commented_times ; ctx._source.gmt_modified=params.gmt_modified",
                                        "params": {
                                            "clicks_times": int(views),
                                            "commented_times": int(replies),
                                            "gmt_modified": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                                        }
                                    }
                                }
                                es.update(index="topic", doc_type="_doc", id=_id, body=insert_body)
                except Exception as e:
                    logger.warning(e)

if __name__ == '__main__':
    a = Analysis()
    a.exquisite()
    a.update()