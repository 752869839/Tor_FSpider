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
                        "query": "c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion"
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
                if record["_source"]["url"][0:84] == 'http://c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion/product/detail':

                    crawl_time = record["_source"]["crawl_time"]

                    domain = 'c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion'

                    net_type = 'tor'

                    spider_name = 'onion_c2p3h_market_spider'

                    try:
                        goods_name = response.xpath('//h2/text()')[0].strip()
                    except:
                        goods_name = ''

                    try:
                        goods_id = record["_source"]["url"]
                        goods_id = re.findall(r'detail/([\s|\S]+)', goods_id)[0]
                    except:
                        goods_id = ''

                    url = record["_source"]["url"]

                    try:
                        goods_info = ''
                        info = response.xpath('//div[@class="detail-body photos"]/text()')
                        for i in info:
                            goods_info += i + '\n'
                    except:
                        goods_info = ''

                    try:
                        goods_img_url = []
                        img_url = response.xpath('//div[@class="detail-body photos"]/img/@src')[
                            0]  # 图片
                        img_url = 'http://c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion' + img_url
                        goods_img_url.append(img_url)
                    except:
                        goods_img_url = []

                    crawl_category = None

                    try:
                        sold_count = re.findall('销售量：(\d+)', html)[0]
                        sold_count = int(sold_count)
                    except:
                        sold_count = None

                    try:
                        price = re.findall('价格：(.*?)</a', html)
                    except:
                        price = []

                    try:
                        user_id = re.findall(r'商户昵称：(.*?)</p', html)[0]
                    except:
                        user_id = ''

                    try:
                        user_name = re.findall(r'商户昵称：(.*?)</p', html)[0]
                    except:
                        user_name = ''

                    goods_area = ''
                    raw_publish_time = ''
                    publish_time = None
                    sku = ''

                    bitcoin_addresses = bitcoin_extract(goods_info)
                    eth_addresses = eth_extract(goods_info)

                    id = sim_hash.g_id(spider_name, goods_id)
                    actions = [{
                        "_index": 'goods',
                        "_type": '_doc',
                        "_op_type": 'create',
                        "_id": id,
                        "_source": {
                            "crawl_time": crawl_time,
                            "domain": domain,
                            "net_type": net_type,
                            "spider_name": spider_name,
                            "goods_name": goods_name,
                            "goods_id": goods_id,
                            "url": url,
                            "goods_info": goods_info,
                            "goods_img_url": goods_img_url,
                            "crawl_category": crawl_category,
                            "sold_count": sold_count,
                            "price": price,
                            "user_id": user_id,
                            "user_name": user_name,
                            "goods_area": goods_area,
                            "raw_publish_time": raw_publish_time,
                            "publish_time": publish_time,
                            "sku": sku,
                            "bitcoin_addresses": bitcoin_addresses,
                            "eth_addresses": eth_addresses,
                            "gmt_create": record["_source"]["gmt_create"],
                            "gmt_modified": record["_source"]["gmt_modified"],
                        }
                    }]
                    success, _ = bulk(es, actions, index='goods', raise_on_exception=False, raise_on_error=False)

                # topic
                if record["_source"]["url"][0:76] == 'http://c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion/posts/':

                    spider_name = 'onion_c2p3h_market_spider'

                    domain = 'c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion'

                    url = record["_source"]["url"]

                    page_index_id = record["_id"]

                    net_type = 'tor'
                    topic_type = 'post'
                    crawl_tags = '楼兰城'

                    try:
                        title = response.xpath('//h1/text()')[0]
                    except:
                        title = ''

                    try:
                        topic_id = record["_source"]["url"]
                        topic_id = re.findall(r'posts/(.*?)/detail', topic_id)[0].strip()
                    except:
                        topic_id = ''

                    try:
                        user_id = response.xpath('//a[@class="fly-link"]/@href')[0].strip()
                        user_id = re.findall('home/([\s|\S]+)', user_id)[0]
                    except:
                        user_id = ''

                    try:
                        user_name = response.xpath('//a[@class="fly-link"]/cite/text()')[0].strip()
                    except:
                        user_name = ''

                    commented_user_id = ''
                    comment_id = ''

                    try:
                        raw_content = response.xpath('//div[@class="detail-body photos"]')[0]
                        raw_content = etree.tostring(raw_content, encoding='utf-8')
                        raw_content = str(raw_content, encoding='utf-8')
                    except:
                        raw_content = ''

                    try:
                        contents = response.xpath('//div[@class="detail-body photos"][1]')
                        content = contents[0].xpath('string(.)')
                    except:
                        content = ''

                    try:
                        clicks_times = int(response.xpath('//span[@class="fly-list-nums"]/text()')[2].replace('\n','').replace(' ',''))
                    except:
                        clicks_times = None

                    try:
                        commented_times = int(response.xpath('//span[@class="fly-list-nums"]/a/text()')[0])
                    except:
                        commented_times = None

                    crawl_time = record["_source"]["crawl_time"]

                    try:
                        raw_publish_time = response.xpath('//div[@class="fly-detail-user"]/span/text()')[0]
                        logger.info(raw_publish_time)
                    except:
                        raw_publish_time = ''

                    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    today = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
                    if '月' in raw_publish_time:
                        num = int(re.findall('(\d+)个', raw_publish_time)[0])
                        publish_time = today - relativedelta(months=num)
                        publish_time = publish_time - relativedelta(hours=8)
                        print(publish_time)

                    elif '天' in raw_publish_time:
                        num = int(re.findall('(\d+)天', raw_publish_time)[0])
                        publish_time = today - relativedelta(days=num)
                        publish_time = publish_time - relativedelta(hours=8)
                        print(publish_time)

                    else:
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

                    p = response.xpath('//div[@id="flyReply"]/ul/li')
                    if len(p) > 1:
                        poster_list = response.xpath('//div[@id="flyReply"]/ul/li')
                        poster_lenght = len(poster_list)
                        for index in range(1, poster_lenght):
                            poster = poster_list[index]

                            spider_name = 'onion_c2p3h_market_spider'

                            domain = 'c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion'

                            url = record["_source"]["url"]

                            page_index_id = record["_id"]

                            net_type = 'tor'
                            topic_type = 'comment'
                            crawl_tags = '楼兰城'

                            try:
                                title = response.xpath('//h1/text()')[0]
                                logger.info(title)
                            except:
                                title = ''

                            try:
                                topic_id = record["_source"]["url"]
                                topic_id = re.findall(r'posts/(.*?)/detail', topic_id)[0].strip()
                            except:
                                topic_id = ''

                            try:
                                user_id = poster.xpath('div//a[@class="fly-link"]/@href')[0].strip()
                                user_id = re.findall('home/([\s|\S]+)', user_id)[0]
                            except:
                                user_id = ''

                            try:
                                user_name = user_name = poster.xpath('div//a[@class="fly-link"]/cite/text()')[0].strip()
                            except:
                                user_name = ''

                            try:
                                commented_user_id = response.xpath('//a[@class="fly-link"]/@href')[0].strip()
                                commented_user_id = re.findall('home/([\s|\S]+)', commented_user_id)[0]
                            except:
                                commented_user_id = ''

                            try:
                                comment_id = poster.xpath('@data-id')[0].strip()
                            except:
                                comment_id = ''

                            try:
                                raw_content = etree.tostring(poster, encoding='utf-8')
                                raw_content = str(raw_content, encoding='utf-8')
                            except:
                                raw_content = ''

                            try:
                                contents = poster.xpath('div[@class="detail-body jieda-body photos"]')
                                content = contents[0].xpath('string(.)')
                            except:
                                content = ''

                            clicks_times = None
                            try:
                                commented_times = int(poster.xpath('div//span[@class="jieda-zan "]/em/text()')[0])
                            except:
                                commented_times = None

                            crawl_time = record["_source"]["crawl_time"]

                            try:
                                raw_publish_time = poster.xpath('div//div[@class="detail-hits"]/span/text()')[0]
                                logger.info(raw_publish_time)
                            except:
                                raw_publish_time = ''

                            t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                            today = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
                            if '月' in raw_publish_time:
                                num = int(re.findall('(\d+)个', raw_publish_time)[0])
                                publish_time = today - relativedelta(months=num)
                                publish_time = publish_time - relativedelta(hours=8)
                                print(publish_time)

                            elif '天' in raw_publish_time:
                                num = int(re.findall('(\d+)天', raw_publish_time)[0])
                                publish_time = today - relativedelta(days=num)
                                publish_time = publish_time - relativedelta(hours=8)
                                print(publish_time)

                            else:
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
                                    #"clicks_times": clicks_times,
                                    "commented_times": commented_times,
                                    "crawl_time": crawl_time,
                                    "publish_time": publish_time,
                                    "raw_publish_time": raw_publish_time,
                                    # "thumbs_up": thumbs_up,
                                    # "thumbs_down": thumbs_down,
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
                        "query": "c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion"
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

            if record["_source"]["url"][0:77] == 'http://c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion/product' and 'detail' not in record["_source"]["url"]:
                try:
                    urls = response.xpath('//table[@class="table table-border-bottom"]//tr/td[1]/a/@href|//table[@class="table table-border-bottom"]//tr/td[2]/a/text()|//table[@class="table table-border-bottom"]//tr/td[4]/text()')
                    urls = [x for x in urls]
                    data = []
                    index_url = 'http://c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion'
                    for index in range(0, len(urls), 3):
                        if index > 0:
                            list_info = urls[index - 3:index]
                            list_info[0] = index_url + list_info[0]
                            data.append(list_info)

                    for j in range(0, len(data)):
                        url = data[j][0]
                        logger.info(url)

                        crawl_category = data[j][1]
                        logger.info(crawl_category)

                        raw_publish_time = data[j][2]
                        logger.info(raw_publish_time)

                        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        today = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
                        if '月' in raw_publish_time:
                            num = int(re.findall('(\d+)个', raw_publish_time)[0])
                            publish_time = today - relativedelta(months=num)
                            publish_time = publish_time - relativedelta(hours=8)
                            print(publish_time)
                        elif '小时' in raw_publish_time:
                            num = int(re.findall('(\d+)小', raw_publish_time)[0])
                            publish_time = today - relativedelta(hours=num)
                            publish_time = publish_time - relativedelta(hours=8)
                            print(publish_time)

                        elif '天' in raw_publish_time:
                            num = int(re.findall('(\d+)天', raw_publish_time)[0])
                            publish_time = today - relativedelta(days=num)
                            publish_time = publish_time - relativedelta(hours=8)
                            print(publish_time)

                        else:
                            publish_time = None

                        goods_id = re.findall(r'detail/([\s|\S]+)', url)[0]
                        print('goods_id:',goods_id)

                        search_query = {
                            "query": {
                                "match_phrase": {
                                    "goods_id": {
                                        "query": goods_id
                                    }
                                }
                            }
                        }
                        r = es.search(index='goods', doc_type='_doc', scroll='50m', body=search_query, timeout='50m')
                        res_lst = r["hits"]["hits"]
                        for rec in res_lst:
                            if goods_id in rec["_source"]["url"]:
                                _id = rec["_id"]
                                insert_body = {
                                    "script": {
                                        "source": "ctx._source.crawl_category=params.crawl_category ;ctx._source.raw_publish_time=params.raw_publish_time ; ctx._source.publish_time=params.publish_time ; ctx._source.gmt_modified=params.gmt_modified",
                                        "params": {
                                            "crawl_category": crawl_category,
                                            "raw_publish_time": raw_publish_time,
                                            "publish_time": publish_time,
                                            "gmt_modified": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
                                        }
                                    }
                                }
                                es.update(index="goods", doc_type="_doc", id=_id, body=insert_body)
                except Exception as e:
                    logger.info(e)


if __name__ == '__main__':
    a = Analysis()
    a.exquisite()
    a.update()