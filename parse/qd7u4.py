# -*- coding: utf-8 -*-
import json
import time
import htmlmin
import re
from lxml import etree
from datetime import datetime
from dateutil.relativedelta import relativedelta
from elasticsearch6.helpers import bulk, scan
import sim_hash
from config import client,es
from bit_eth_ema import bitcoin_extract,eth_extract,email_extract
from log_decorator import _logger, exception_logger

logger = _logger()

def key():
    length = re_queue.llen('onion_qd7u4_blog_spider:items')
    logger.info(length)
    # logger.info(type(length))
    if length > 10:
        write_table()
        exquisite()

def l_push():
    re_queue.lpush("qd7u4:start_url", "http://4qd7u4c5s6iezmp2.onion/")


def write_table():
    try:
        while True:
            time.sleep(0.01)
            start_time = time.time()
            source, data = client.blpop(["onion_qd7u4_blog_spider:items"], timeout=100)
            data = json.loads(data.decode("utf-8"))
            page_id = sim_hash.p_id(data['domain'], htmlmin.minify(data['raw_text'].encode('utf-8').decode('utf-8'),
                                                                   remove_all_empty_space=True))
            false = False
            actions = [{
                "_index": 'page',
                "_type": '_doc',
                "_op_type": 'create',
                "_id": page_id,
                "_source": {
                    "spider_name":'onion_qd7u4_blog_spider',
                    "crawl_time": data['crawl_time'],
                    "net_type": data['net_type'],
                    "url": data['url'],
                    "h1": data['h1'],
                    "title": data['raw_title'],
                    "meta": data['meta'],
                    "headers": data['headers'],
                    "raw_text": htmlmin.minify(data['raw_text'].encode('utf-8').decode('utf-8'),remove_all_empty_space=True),
                    "domain": data['domain'],
                    "language": data['language'],
                    "content_type": data['content_type'],
                    "content_encode": data['content_encode'],
                    "code": data['code'],
                    "links":data['links'],
                    "is_fake": false,
                    "is_banned": false,
                    "is_extracted": false,
                    "is_analyzed": false,
                    "gmt_create": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                    "gmt_modified": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                }
            }]
            success, _ = bulk(es, actions, index='page', raise_on_exception=False, raise_on_error=False)
            end_time = time.time()
            logger.info(end_time - start_time)
    except Exception as e:
        logger.warning(e)


def exquisite():
    search_query = {
        "query": {
            "match_phrase": {
                "domain": {
                    "query": "4qd7u4c5s6iezmp2.onion"
                }
            }
        }
    }
    start_time = time.time()
    actions = []
    res = scan(client=es, query=search_query, scroll='50m', index='page', doc_type='_doc', timeout='1m')
    cnt = 0
    for record in res:
        print(cnt, record["_source"]["url"])
        cnt += 1
        html = record["_source"]["raw_text"]
        response = etree.HTML(html)

        # topic
        if record["_source"]["url"][0:37] == 'http://4qd7u4c5s6iezmp2.onion/en/blog' and len(record["_source"]["url"]) > 62:

            spider_name = 'onion_qd7u4_blog_spider'

            domain = '4qd7u4c5s6iezmp2.onion'

            url = record["_source"]["url"]

            page_index_id = record["_id"]

            net_type = 'tor'

            topic_type = 'news'

            try:
                crawl_tags = response.xpath('//div[@class="views-field views-field-field-blog-category"]/div/a/text()')
            except:
                crawl_tags = []

            try:
                title = response.xpath('//h1[@class="field-content node-blog-entry-title"]/text()')[0].strip()
            except:
                title = ''

            try:
                topic_id = record["_source"]["url"]
                topic_id = re.findall(r'blog/([\s|\S]+)', topic_id)[0]
            except:
                topic_id = ''

            user_id = 'Stephan Altmann'
            user_name = 'Stephan Altmann'
            commented_user_id = ''
            comment_id = ''

            try:
                raw_content = response.xpath('//div[@class="views-row"]')[0]
                raw_content = etree.tostring(raw_content, encoding='utf-8')
                raw_content = str(raw_content,encoding='utf-8')
            except:
                raw_content = ''

            try:
                contents = response.xpath('//div[@class="views-row"]')
                content = contents[0].xpath('string(.)')
            except:
                content = ''

            clicks_times = None
            commented_times = None
            crawl_time = record["_source"]["crawl_time"]

            try:
                raw_publish_time = response.xpath('//span[@class="field-content blog-entry-date"]/text()')[0].strip().replace('.', '')
            except:
                raw_publish_time = ''

            try:
                publish_time = datetime.strptime(raw_publish_time, '%j %B %Y')
                publish_time = publish_time - relativedelta(hours=8)
            except:
                publish_time = None

            thumbs_up = None
            thumbs_down = None


            emails = email_extract(content)

            bitcoin_addresses = bitcoin_extract(content)

            eth_addresses = eth_extract(content)


            false = False

            id = sim_hash.t_id(spider_name, topic_id, user_id, raw_content, comment_id)
            action1 = {
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
                    "is_extracted": false,
                    "is_analyzed": false,
                    "gmt_create": record["_source"]["gmt_create"],
                    "gmt_modified": record["_source"]["gmt_modified"],
                }
            }
            actions.append(action1)
        success, _ = bulk(es, actions, index='topic', raise_on_exception=False, raise_on_error=False)
        actions.clear()
        end_time = time.time()
        logger.info(end_time - start_time)



if __name__ == '__main__':
    key()
