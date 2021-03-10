# -*- coding: utf-8 -*-
import time
import json
import htmlmin
from lxml import etree
from datetime import datetime
from multiprocessing import Process
from elasticsearch6.helpers import bulk
import sim_hash
from config import client,es
from log_decorator import _logger, exception_logger

logger = _logger()

def transfer_redis_es(spider_name):
    n = 0
    while True:
        time.sleep(0.01)
        try:
            source, redis_data = client.blpop(["{}:items".format(spider_name)])
            redis_data = json.loads(redis_data.decode("utf-8"))
            response = etree.HTML(redis_data['raw_text'])
            try:
                ele = response.xpath('//script | //noscript | //style')
                for e in ele:
                    e.getparent().remove(e)
            except Exception as e:
                pass
            contents = response.xpath("//html//body")[0].xpath("string(.)")
            try:
                links = redis_data['links']
            except:
                links = []

            page_id = sim_hash.p_id(redis_data['domain'], htmlmin.minify(redis_data['raw_text'].encode('utf-8').decode('utf-8'),remove_all_empty_space=True))
            actions = [{
                "_index": 'page',
                "_id":page_id,
                "_type": '_doc',
                "_source" : {
                    "spider_name": spider_name,
                    "url": redis_data['url'],
                    "crawl_time": redis_data['crawl_time'],
                    "domain": redis_data['domain'],
                    "title": redis_data['raw_title'],
                    "raw_text": htmlmin.minify(redis_data['raw_text'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True),
                    # "content":contents,
                    "language": redis_data['language'],
                    "net_type": redis_data['net_type'],
                    "h1": redis_data['h1'],
                    "meta": redis_data['meta'],
                    "headers": redis_data['headers'],
                    "content_type": redis_data['content_type'],
                    "content_encode": redis_data['content_encode'],
                    "code": redis_data['code'],
                    "links": links,
                    "gmt_create": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                    "gmt_modified": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                }
            }]
            success, _ = bulk(es, actions, index='page',raise_on_error=True)
            n = n + 1
            print(n, redis_data['url'])
        except Exception as e:
            logger.warning(e)

@exception_logger(logger)
def task_schdule():
    processes = []
    for i, spider_name in enumerate(spider_names):
        process = Process(target=transfer_redis_es, args=(spider_name,))
        processes.append(process)
        processes[i].start()


if __name__ == '__main__':
    spider_names = ['onion_agarth_market_spider','onion_alibaba_market_spider','onion_apollo_market_spider','onion_avenger_bbs_spider','onion_c2p3h_market_spider','onion_cryptbbs_bbs_spider','onion_facebook_bbs_spider','onion_guns_market_spider','onion_gw6zz_market_spider','onion_horoio_blog_spider','onion_ninan_market_spider','onion_hour24_market_spider','onion_jesblog_blog_spider','onion_lfwpm_bbs_spider','onion_nytime_new_spider','onion_pncld_bbs_spider','onion_sfdu2_market_spider','onion_shopt_market_spider','onion_torum_bbs_spider','onion_xbtpp_market_spider','onion_xs6qb_market_spider','onion_yue4e_market_spider','onion_zj4o7_market_spider']
    task_schdule()
