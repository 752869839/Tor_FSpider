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
                        "query": "lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion"
                    }
                }
            }
        }

        res = scan(client=es, query=search_query, scroll='5m', index='page', doc_type='_doc', timeout='1m')
        cnt = 0
        for record in res:
            print(cnt, record["_source"]["url"])
            cnt += 1
            html = record["_source"]["raw_text"]
            response = etree.HTML(html.encode('utf-8'))
            try:
                # topic
                if record["_source"]["url"][
                   0:76] == 'http://lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion/thread':

                    spider_name = 'onion_lfwpm_bbs_spider'

                    domain = 'lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion'

                    url = record["_source"]["url"]

                    page_index_id = record["_id"]

                    net_type = 'tor'

                    topic_type = 'post'

                    try:
                        crawl_tags = response.xpath('//div[@class="z"]/a[4]/text()')
                    except:
                        crawl_tags = []

                    try:
                        title = response.xpath('//span[@id="thread_subject"]/text()')[0].strip()
                    except:
                        title = ''

                    try:
                        topic_id = record["_source"]["url"]
                        topic_id = re.findall(r'thread-(.*?).html', topic_id)[0]
                    except:
                        topic_id = ''

                    try:
                        user_id = response.xpath('//a[@class="xw1"]/@href')[0]
                        user_id = re.findall('space-uid-(.*?).html', user_id)[0]
                    except:
                        user_id = ""

                    try:
                        user_name = response.xpath('//a[@class="xw1"]/text()')[0]
                    except:
                        user_name = ""

                    commented_user_id = ''
                    comment_id = ''

                    try:
                        raw_content = response.xpath('//table[@class="plhin"]')[0]
                        raw_content = etree.tostring(raw_content, encoding='utf-8')
                        raw_content = str(raw_content, encoding='utf-8')
                    except:
                        raw_content = ''

                    try:
                        contents = response.xpath('//table[@class="plhin"]')
                        content = contents[0].xpath('string(.)')
                    except:
                        content = ''

                    try:
                        clicks_times = int(response.xpath('//span[@class="xi1"]/text()')[0])
                    except:
                        clicks_times = None

                    try:
                        commented_times = int(response.xpath('//span[@class="xi1"]/text()')[1])
                    except:
                        commented_times = None

                    crawl_time = record["_source"]["crawl_time"]

                    try:
                        raw_publish_time = response.xpath('//div[@class="authi"]/em/text()')[0].replace('发表于 ', '').replace('-**', '')
                        raw_publish_time = str(raw_publish_time)
                    except:
                        raw_publish_time = ''

                    try:
                        publish_time = datetime.strptime(raw_publish_time, '%Y-%m')
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
                            "thumbs_up": thumbs_up,
                            "thumbs_down": thumbs_down,
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
