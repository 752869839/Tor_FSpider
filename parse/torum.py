# -*- coding: utf-8 -*-
import time
import re
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
                        "query": "torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion"
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
                if record["_source"]["url"][
                   0:83] == 'http://torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion/viewtopic.php':

                    spider_name = 'onion_torum_bbs_spider'

                    domain = 'torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion'

                    net_type = 'tor'

                    try:
                        user_name = response.xpath('//span[@class="responsive-hide"]/strong/span/text()')[0].strip()
                    except:
                        user_name = ''

                    user_description = ''

                    try:
                        user_id = response.xpath('//span[@class="responsive-hide"]/strong/span/text()')[0].strip()
                    except:
                        user_id = ''

                    url = record["_source"]["url"]

                    try:
                        raw_register_time = response.xpath('//dd[@class="profile-joined"]/text()')[0].strip()
                    except:
                        raw_register_time = ''

                    try:
                        register_time = datetime.strptime(raw_register_time, '%d %b %Y')
                        register_time = register_time - relativedelta(hours=8)
                    except:
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

                    try:
                        member_degree = response.xpath('//dd[@class="profile-rank rank-img"]/text()')[0].strip()
                    except:
                        member_degree = ""

                    pgp = ''

                    crawl_time = record["_source"]["crawl_time"]

                    try:
                        topic_nums = response.xpath('//dd[@class="profile-posts"]/a/text()')[0].strip()
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
                            #"last_active_time": last_active_time,
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
                if record["_source"]["url"][
                   0:83] == 'http://torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion/viewtopic.php':

                    spider_name = 'onion_torum_bbs_spider'

                    domain = 'torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion'

                    url = record["_source"]["url"]

                    page_index_id = record["_id"]

                    net_type = 'tor'

                    topic_type = 'post'

                    try:
                        crawl_tags = response.xpath('//span[@itemprop="title"]/text()')
                    except:
                        crawl_tags = []

                    try:
                        title = response.xpath('//h2[@class="topic-title"]/a/text()')[0].strip()
                    except:
                        title = ''

                    try:
                        topic_id = record["_source"]["url"]
                        topic_id = re.findall(r't=(.*?)&', topic_id)[0].strip()
                    except:
                        topic_id = record["_source"]["url"]
                        topic_id = re.findall(r't=([\s|\S]+)', topic_id)[0].strip()

                    try:
                        user_id = response.xpath('//span[@class="responsive-hide"]/strong/span/text()')[0].strip()
                    except:
                        user_id = ''

                    try:
                        user_name = response.xpath('//span[@class="responsive-hide"]/strong/span/text()')[0].strip()
                    except:
                        user_name = ''

                    commented_user_id = ''
                    comment_id = ''

                    try:
                        raw_content = response.xpath('//div[@class="postbody"]/div/div')[0]
                        raw_content = etree.tostring(raw_content, encoding='utf-8')
                        raw_content = str(raw_content, encoding='utf-8')
                    except:
                        raw_content = ''

                    try:
                        contents = response.xpath('//div[@class="content"][1]')
                        content = contents[0].xpath('string(.)')
                    except:
                        content = ''

                    clicks_times = None
                    commented_times = None

                    crawl_time = record["_source"]["crawl_time"]

                    try:
                        raw_publish_time = response.xpath('//p[@class="author"]/time/text()')[0].strip()
                    except:
                        raw_publish_time = ''

                    try:
                        data_time = response.xpath('//p[@class="author"]/time/@datetime')[0].strip()[0:19]
                        # publish_time = datetime.strptime(raw_publish_time, '%d %b %Y')
                        # publish_time = publish_time - relativedelta(hours=8)
                        publish_time = datetime.strptime(data_time, '%Y-%m-%dT%H:%M:%S')
                    except:
                        publish_time = None

                    try:
                        thumbs_ups = response.xpath('//p[@class="author"]')
                        thumbs_up = int(len(thumbs_ups))
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

                    p = response.xpath('//div[@id="page-body"]/div')
                    if len(p) > 2:
                        poster_list = response.xpath(
                            '//div[@id="page-body"]/div[@class="post has-profile bg2 unreadpost" or @class="post has-profile bg1 unreadpost" or @class="post has-profile bg2" or @class="post has-profile bg1"] ')
                        poster_lenght = len(poster_list)
                        for index in range(1, poster_lenght):
                            poster = poster_list[index]

                            spider_name = 'onion_torum_bbs_spider'

                            domain = 'torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion'

                            net_type = 'tor'

                            try:
                                user_name = poster.xpath('div/div/div/p/span/strong/span/text()')[0].strip()
                            except:
                                user_name = ''

                            user_description = ''

                            try:
                                user_id = poster.xpath('div/div/div/p/span/strong/span/text()')[0].strip()
                            except:
                                user_id = ''

                            url = record["_source"]["url"]

                            try:
                                raw_register_time = poster.xpath('div/dl/dd[@class="profile-joined"]/text()')[0].strip()
                            except:
                                raw_register_time = ''

                            try:
                                register_time = datetime.strptime(raw_register_time, '%d %b %Y')
                                register_time = register_time - relativedelta(hours=8)
                            except:
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

                            try:
                                member_degree = poster.xpath('div/dl/dd[@class="profile-rank rank-img"]/text()')[0].strip()
                            except:
                                member_degree = ""

                            pgp = ''

                            crawl_time = record["_source"]["crawl_time"]


                            try:
                                topic_nums = poster.xpath('div/dl/dd[@class="profile-posts"]/a/text()')[0].strip()
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
                                    #"last_active_time": last_active_time,
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


                    p = response.xpath('//div[@id="page-body"]/div')
                    if len(p) > 2:
                        poster_list = response.xpath(
                            '//div[@id="page-body"]/div[@class="post has-profile bg2 unreadpost" or @class="post has-profile bg1 unreadpost" or @class="post has-profile bg2" or @class="post has-profile bg1"] ')
                        poster_lenght = len(poster_list)
                        for index in range(1, poster_lenght):
                            poster = poster_list[index]

                            spider_name = 'onion_torum_bbs_spider'

                            domain = 'torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion'

                            url = record["_source"]["url"]

                            page_index_id = record["_id"]

                            net_type = 'tor'

                            topic_type = 'comment'

                            try:
                                crawl_tags = response.xpath('//span[@itemprop="title"]/text()')
                            except:
                                crawl_tags = []

                            try:
                                title = response.xpath('//h2[@class="topic-title"]/a/text()')[0].strip()
                            except:
                                title = ''

                            try:
                                topic_id = record["_source"]["url"]
                                topic_id = re.findall(r't=(.*?)&', topic_id)[0].strip()
                            except:
                                topic_id = record["_source"]["url"]
                                topic_id = re.findall(r't=([\s|\S]+)', topic_id)[0].strip()

                            try:
                                user_id = poster.xpath('div/div/div/p/span/strong/span/text()')[0].strip()
                            except:
                                user_id = ''

                            try:
                                user_name = poster.xpath('div/div/div/p/span/strong/span/text()')[0].strip()
                            except:
                                user_name = ''

                            try:
                                commented_user_id = \
                                response.xpath('//span[@class="responsive-hide"][1]/strong/a/@href')[0]
                                commented_user_id = re.findall(r'u=([\s|\S]+)', commented_user_id)[0]
                            except:
                                commented_user_id = ''

                            try:
                                comment_id = poster.xpath('@id')[0].strip().replace('p', '')
                            except:
                                comment_id = ''

                            try:
                                raw_content = poster.xpath('div//div[@class="postbody"]/div/div')[0]
                                raw_content = etree.tostring(raw_content, encoding='utf-8')
                                raw_content = str(raw_content, encoding='utf-8')
                            except:
                                raw_content = ''

                            try:
                                contents = poster.xpath('div//div[@class="content"]')
                                content = contents[0].xpath('string(.)')
                            except:
                                content = ''

                            clicks_times = None
                            commented_times = None

                            crawl_time = record["_source"]["crawl_time"]

                            try:
                                raw_publish_time = poster.xpath('div/div/div/p/time/text()')[0]
                            except:
                                raw_publish_time = ''

                            try:

                                # publish_time = datetime.strptime(raw_publish_time, '%d %b %Y')
                                # publish_time = publish_time - relativedelta(hours=8)
                                data_time = poster.xpath('div/div/div/p/time/@datetime')[0][0:19]
                                publish_time = datetime.strptime(data_time, '%Y-%m-%dT%H:%M:%S')
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
            # "size":1000,
            "query": {
                "match_phrase": {
                    "domain": {
                        "query": "torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion"
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
            if record["_source"]["url"][0:84] == 'http://torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion/viewforum.php?':
                try:
                    urls = response.xpath(
                            '//a[@class="topictitle"]/@href|//ul[@class="topiclist topics"]//dl/dd[1]/text()|//ul[@class="topiclist topics"]//dl/dd[2]/text()')
                    print(urls)
                    data = []
                    index_url = 'http://torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion/'
                    for index in range(0, len(urls), 3):
                        if index > 0:
                            list_info = urls[index - 3:index]
                            list_info[0] = index_url + list_info[0].replace('./', '')
                            data.append(list_info)
                    for j in range(0, len(data)):
                        url = data[j][0]

                        replies = data[j][1]

                        views = data[j][2]

                        topic_id = re.findall(r't=([\s|\S]+)', url)[0].strip()
                        print('topic_id:', topic_id)

                        search_query = {
                            "query": {
                                "bool": {
                                    "must": [
                                        {"match": {
                                            "domain": "torum43tajnrxritn4iumy75giwb5yfw6cjq2czjikhtcac67tfif2yd.onion"}},
                                        {"match": {
                                            "topic_id": topic_id}}
                                    ]
                                }
                            }
                        }
                        r = es.search(index='topic', doc_type='_doc', body=search_query, timeout='500m')
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