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
from mylog import logger, exception_logger

logger = logger()

class Analysis(object):
    def exquisite(self):
        search_query = {
            "query": {
                "match_phrase": {
                    "domain": {
                        "query": "pncldyerk4gqofhp.onion"
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
                if record["_source"]["url"][0:41] == 'http://pncldyerk4gqofhp.onion/free/thread':
                    spider_name = 'onion_pncld_bbs_spider'

                    domain = 'pncldyerk4gqofhp.onion'

                    net_type = 'tor'

                    try:
                        user_name = response.xpath(
                            '//span[@class="profile-username"]/a/text()|//span[@class="profile-username"]/a/span/text()')[
                            0]
                    except:
                        user_name = ''

                    user_description = ''

                    try:
                        user_id = response.xpath('//span[@class="profile-username"]/a/@href')[0]
                        user_id = re.findall(r'user-(.*?).html', user_id)[0]
                    except:
                        user_id = ''

                    url = record["_source"]["url"]
                    raw_register_time = ''
                    register_time = None
                    user_img_url = ''

                    emails = email_extract(user_description)

                    bitcoin_addresses = bitcoin_extract(user_description)

                    eth_addresses = eth_extract(user_description)

                    try:
                        raw_last_active_time = response.xpath('//span[@class="post_date"][1]/text()')[0].strip()
                    except:
                        raw_last_active_time = ''

                    try:
                        last_active_time = datetime.strptime(raw_last_active_time, '%m-%d-%Y')
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
                if record["_source"]["url"][0:41] == 'http://pncldyerk4gqofhp.onion/free/thread':

                    spider_name = 'onion_pncld_bbs_spider'

                    domain = 'pncldyerk4gqofhp.onion'

                    url = record["_source"]["url"]

                    page_index_id = record["_id"]

                    net_type = 'tor'

                    topic_type = 'post'

                    try:
                        crawl_tags = response.xpath('//div[@class="navigation"]/span/a[3]/text()')[0]
                    except:
                        crawl_tags = ''

                    try:
                        title = response.xpath('//td[@class="thead"]/strong/text()')[0]
                    except:
                        title = ''

                    try:
                        topic_id = record["_source"]["url"]
                        topic_id = re.findall(r'thread-(.*?)-page', topic_id)[0]
                    except:
                        topic_id = record["_source"]["url"]
                        topic_id = re.findall(r'thread-(.*?).html', topic_id)[0]

                    try:
                        user_id = response.xpath('//span[@class="profile-username"]/a/@href')[0]
                        user_id = re.findall(r'user-(.*?).html', user_id)[0]
                    except:
                        user_id = ''

                    try:
                        user_name = response.xpath(
                            '//span[@class="profile-username"]/a/text()|//span[@class="profile-username"]/a/span/text()')[
                            0]
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
                        contents = response.xpath('//div[@class="post_body scaleimages"]/text()')  # xpath匹配得到所有的数据
                        a = ''.join(contents)  # 将匹配得到列表数据拼接成字符串
                        b = response.xpath('//div[@class="post_body scaleimages"]')  # 匹配单个div数据
                        d = []  # 定义空列表存放数据
                        for i in b:  # 遍历每个div的数据
                            c = i.text  # 将每个div元素的强行转为text，得到每级第一个
                            d.append(c)  # 将div的第一个添加到列表中
                        e = d[1]  # 取出第二个div的文本
                        f = a.split(e)  # 通过第二个div的文本进行切割分离
                        content = f[0]  # 取出第0个元素
                    except:
                        content = ''

                    clicks_times = None
                    commented_times = None
                    crawl_time = record["_source"]["crawl_time"]

                    try:
                        raw_publish_time = response.xpath('//span[@class="post_date"][1]/text()')[0].strip()
                    except:
                        raw_publish_time = ''

                    try:
                        publish_time = datetime.strptime(raw_publish_time, '%m-%d-%Y')
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

                # user
                p = response.xpath('//div[@id="posts"]/div[@class="posts2 post classic "]')
                if len(p) > 1:
                    poster_list = response.xpath('//div[@id="posts"]/div[@class="posts2 post classic "]')
                    poster_lenght = len(poster_list)
                    for index in range(1, poster_lenght):
                        poster = poster_list[index]

                        spider_name = 'onion_pncld_bbs_spider'

                        domain = 'pncldyerk4gqofhp.onion'

                        net_type = 'tor'

                        try:
                            user_name = poster.xpath('div[@id="one"]//a/text()')[0].strip()
                        except:
                            user_name = ''

                        user_description = ''

                        try:
                            user_ids = poster.xpath('div//span[@class="profile-username"]/a/@href')[0]
                            user_id = re.findall(r'user-(.*?).html', user_ids)[0]
                        except:
                            user_id = ''

                        url = record["_source"]["url"]
                        raw_register_time = ''
                        register_time = None
                        user_img_url = ''

                        emails = email_extract(user_description)

                        bitcoin_addresses = bitcoin_extract(user_description)

                        eth_addresses = eth_extract(user_description)

                        try:
                            raw_last_active_time = poster.xpath('div[@id="two"]/div[1]/span[1]//text()')[0].strip()
                        except:
                            raw_last_active_time = ''

                        try:
                            last_active_time = datetime.strptime(raw_last_active_time, '%m-%d-%Y')
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
                p = response.xpath('//div[@id="posts"]/div[@class="posts2 post classic "]')
                if len(p) > 1:
                    poster_list = response.xpath('//div[@id="posts"]/div[@class="posts2 post classic "]')
                    poster_lenght = len(poster_list)
                    for index in range(1, poster_lenght):
                        poster = poster_list[index]

                        spider_name = 'onion_pncld_bbs_spider'

                        domain = 'pncldyerk4gqofhp.onion'

                        url = record["_source"]["url"]

                        page_index_id = record["_id"]

                        net_type = 'tor'

                        topic_type = 'comment'

                        try:
                            crawl_tags = response.xpath('//div[@class="navigation"]/span/a[3]/text()')[0]
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
                            user_ids = poster.xpath('div//span[@class="profile-username"]/a/@href')[0]
                            user_id = re.findall(r'user-(.*?).html', user_ids)[0]
                        except:
                            user_id = ''

                        try:
                            user_name = poster.xpath('div[@id="one"]//a/text()')[0].strip()
                        except:
                            user_name = ''

                        try:
                            commented_user_ids = response.xpath('//span[@class="profile-username"]/a/@href')[0]
                            commented_user_id = re.findall(r'user-(.*?).html', commented_user_ids)[0]
                        except:
                            commented_user_id = ''

                        try:
                            comment_id = poster.xpath('@id')[0].strip().replace('post_', '')
                        except:
                            comment_id = ''

                        try:
                            raw_content = etree.tostring(poster, encoding='utf-8')
                            raw_content = str(raw_content, encoding='utf-8')
                        except:
                            raw_content = ''

                        try:
                            content = poster.xpath('div[@id="two"]/div[2]/text()')[0].strip()
                        except:
                            content = ''

                        clicks_times = None
                        commented_times = None
                        crawl_time = record["_source"]["crawl_time"]

                        try:
                            raw_publish_time = poster.xpath('div[@id="two"]/div[1]/span[1]//text()')[0].strip()
                        except:
                            raw_publish_time = ''

                        try:
                            publish_time = datetime.strptime(raw_publish_time, '%m-%d-%Y')
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
            # "size":1000,
            "query": {
                "match_phrase": {
                    "domain": {
                        "query": "pncldyerk4gqofhp.onion"
                    }
                }
            }
        }
        res = scan(client=es, query=search_query, scroll='5m', index='page', doc_type='_doc', timeout='5m')
        cnt = 0
        for record in res:
            cnt += 1
            html = record["_source"]["raw_text"]
            response = etree.HTML(html)
            if record["_source"]["url"][0:40] == 'http://pncldyerk4gqofhp.onion/free/forum':
                try:
                    urls = response.xpath(
                        '//tr[@class="inline_row"]/td[1]/div/span/span[@class=" subject_new" or @class=" subject_old"]//a/@href|//tr[@class="inline_row"]/td[2]/a/text()|//tr[@class="inline_row"]/td[3]/text()')
                    data = []
                    index_url = 'http://pncldyerk4gqofhp.onion/free/'
                    for index in range(0, len(urls), 3):
                        if index > 0:
                            list_info = urls[index - 3:index]
                            list_info[0] = index_url + list_info[0]
                            data.append(list_info)

                    for j in range(0, len(data)):
                        url = data[j][0]
                        logger.info(url)
                        replies = data[j][1]
                        logger.info(replies)
                        views = data[j][2]
                        views = views.replace(',','')
                        logger.info(views)

                        search_query = {
                            # "size":1000,
                            "query": {
                                "match_phrase": {
                                    "domain": {
                                        "query": "pncldyerk4gqofhp.onion"
                                    }
                                }
                            }
                        }
                        r = scan(client=es, query=search_query, scroll='5m', index='topic', doc_type='_doc',
                                 timeout='5m')
                        cnt = 0
                        for rec in r:
                            if url in rec["_source"]["url"]:
                                _id = rec["_id"]
                                insert_body = {
                                    "script": {
                                        "source": "ctx._source.clicks_times=params.clicks_times ; ctx._source.commented_times=params.commented_times ; ctx._source.gmt_modified=params.gmt_modified",
                                        "params": {
                                            "clicks_times": int(replies),
                                            "commented_times": int(views),
                                            "gmt_modified": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
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