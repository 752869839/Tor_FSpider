# -*- coding: utf-8 -*-
import time
from elasticsearch import Elasticsearch

query_es = Elasticsearch(hosts='172.16.30.68', port=9200, timeout=30, max_retries=10)


def domain_query_write():
    search_query = {
        "size": 0,
        "aggs": {
            "domain": {
                "terms": {
                    "field": "domain",
                    "size": 38079
                }
            }
        }
    }
    response = query_es.search(index='extensive', body=search_query)
    cnt = 0
    start_time = time.time()
    res_list = response["aggregations"]["domain"]["buckets"]
    for record in res_list:
        cnt += 1
        end_time = time.time()
        print(cnt, record["key"], end_time - start_time)
        with open('new_domain.txt', 'a+', encoding='utf-8') as f:
            f.write(record["key"] + '\n')
            f.close()

    return None


if __name__ == '__main__':
    domain_query_write()

