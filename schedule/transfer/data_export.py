# -*- coding: utf-8 -*-
import time
import json
import htmlmin
from lxml import etree
from multiprocessing import Process
from elasticsearch.helpers import bulk
from sim_hash import p_id
from extract_arithmetic import phone_extract,qq_extract,wechart_extract,alipay_extract,card_extract,tg_extract,pgp_extract,bitcoin_extract,eth_extract,email_extract,ip_extract,bat_extract,facebook_extract,twitter_extract,keywords,keysentence
from config import redis_client,es_client



def data_tran(spider_name):
    n = 0
    actions = []
    while True:
        time.sleep(0.01)
        try:
            source, redis_data = redis_client.blpop([f"{spider_name}:items"])
            redis_data = json.loads(redis_data.decode("utf-8"))
            response = etree.HTML(redis_data['html'].encode('utf-8'))
            ele = response.xpath('//script | //noscript | //style')
            for e in ele:
                e.getparent().remove(e)
            content = response.xpath("//html//body")[0].xpath("string(.)")
            index = 'intelligence_cloud'
            action = {
                "_index": index,
                "_id": p_id(redis_data['domain'],
                            htmlmin.minify(redis_data['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)),
                # "_type": '_doc',
                "_source": {
                    "url": redis_data['url'],
                    "status": redis_data['status'],
                    "net_type": 'onion',
                    "domain": redis_data['domain'],
                    "description": redis_data['description'],
                    "keywords": keywords(content),
                    "abstract": keysentence(content[0:50000]),
                    "title": redis_data['title'],
                    "html": redis_data['html'],
                    "content": content,
                    "language": redis_data['language'],
                    "encode": redis_data['encode'],
                    # "significance": '',
                    "category": [],
                    "topic": [],
                    # "mirror": [],
                    "phone_number": phone_extract(content),
                    "qq": qq_extract(content),
                    "card_id": card_extract(content),
                    "telegram_id": tg_extract(content),
                    "wechat": wechart_extract(content),
                    "ip": ip_extract(content),
                    "bat": bat_extract(content),
                    "facebook": facebook_extract(content),
                    "twitter": twitter_extract(content),
                    "pgp": pgp_extract(content),
                    "bitcoin_addresses": bitcoin_extract(content),
                    "eth_addresses": eth_extract(content),
                    "emails": email_extract(content),
                    "crawl_time": redis_data['crawl_time'],
                    "gmt_create": redis_data['crawl_time'],
                    "gmt_modified": redis_data['crawl_time'],
                }
            }
            n += 1
            print(n, redis_data['url'])
            actions.append(action)
            if len(actions) == 320:
                success, _ = bulk(es_client, action, index=index, raise_on_error=False)
                print('批量插入成功!')
                actions.clear()
        except Exception as e:
            print(e)

def task_schdule():
    processes = []
    name = 'onion_tor_whole_spider'
    spder_name_list = []
    for i in range(32):
        spder_name_list.append(name)

    for i, spider_name in enumerate(spder_name_list):
        process = Process(target=data_tran, args=(spider_name,))
        processes.append(process)
        processes[i].start()

if __name__ == '__main__':
    task_schdule()
