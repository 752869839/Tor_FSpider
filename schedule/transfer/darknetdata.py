# -*- coding: utf-8 -*-
import time
import json
from lxml import etree
from datetime import datetime
from multiprocessing import Process
from elasticsearch.helpers import bulk
from sim_hash import es_id
from extract_arithmetic import phone_extract,qq_extract,card_extract,tg_extract,pgp_extract,bitcoin_extract,eth_extract,email_extract,ip_extract,bat_extract
from config import redis_client,es_client



def data_tran(spider_name):
    n = 0
    actions = []
    index = 'darknetdata'

    while True:
        time.sleep(0.01)
        try:
            source, redis_data = redis_client.blpop([f"{spider_name}:items"])
            redis_data = json.loads(redis_data.encode('utf-8').decode("utf-8"))
            if redis_data:
                if redis_data['title'] and 'porn' in redis_data['title']  \
                        or 'porn' in redis_data['url']:
                    print('色情网站',redis_data['url'])
                    continue
            response = etree.HTML(redis_data['html'].encode('utf-8'))
            ele = response.xpath('//script | //noscript | //style')
            for e in ele:
                e.getparent().remove(e)
            content = response.xpath("//html//body")[0].xpath("string(.)")
            id = es_id(redis_data['url'])
            search_query = {
              "query": {
                "match": {
                  "_id":id
                }
              }
            }
            res = es_client.search(index=index, body=search_query, timeout='5m')
            if res["hits"]["hits"]:
                insert_body = {
                    "script": {
                        "source": "ctx._source.title=params.title ; ctx._source.html=params.html ; ctx._source.content=params.content ; ctx._source.gmt_modified=params.gmt_modified",
                        "params": {
                            "title": redis_data['title'],
                            "html": redis_data['html'],
                            "content": content,
                            "gmt_modified": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                        }
                    }
                }
                n += 1
                es_client.update(index=index,  id=id, body=insert_body)
                print(n, id, '更新成功')
            else:
                action = {
                    "_index": index,
                    "_id": id,
                    "_source": {
                        "url": redis_data['url'],
                        "status": redis_data['status'],
                        "net_type": 'onion',
                        "domain": redis_data['domain'],
                        "description": redis_data['description'],
                        "title": redis_data['title'],
                        "html": redis_data['html'],
                        "content": content,
                        "language": redis_data['language'],
                        "encode": redis_data['encode'],
                        # "significance": '',
                        "category": [],
                        # "mirror": [],
                        "phone_number": phone_extract(content),
                        "qq": qq_extract(content),
                        "card_id": card_extract(content),
                        "telegram_id": tg_extract(content),
                        "ip": ip_extract(content),
                        "bat": bat_extract(content),
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
                print(n, id)
                actions.append(action)
                if len(actions) == 500:
                    success, _ = bulk(es_client, actions, index=index, raise_on_error=False)
                    print('批量插入成功!')
                    actions.clear()

        except Exception as e:
            print(e)


def task_schdule():
    processes = []
    name = 'onion_tor_whole_spider'
    spder_name_list = []
    for i in range(16):
        spder_name_list.append(name)

    for i, spider_name in enumerate(spder_name_list):
        process = Process(target=data_tran, args=(spider_name,))
        processes.append(process)
        processes[i].start()

if __name__ == '__main__':
    task_schdule()


