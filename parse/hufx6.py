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
from logg import logger
from config import re_queue,client,es
from bit_eth_ema import bitcoin_extract,eth_extract,email_extract


def key():
    length = re_queue.llen('onion_hufx6_bbs_spider:items')
    logger.info(length)
    if length > 10:
        write_table()
        exquisite()

def l_push():
    re_queue.lpush("hufx6:start_url", "http://hufx6h5lcbcmpifa.onion/forum.php")


def write_table():
    try:
        while True:
            time.sleep(0.01)
            start_time = time.time()
            source, data = client.blpop(["onion_hufx6_bbs_spider:items"], timeout=100)
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
                    "spider_name":'onion_hufx6_bbs_spider',
                    "crawl_time": data['crawl_time'],
                    "net_type": data['net_type'],
                    "url": data['url'],
                    "h1": data['h1'],
                    "title": data['raw_title'],
                    "meta": data['meta'],
                    "headers": data['headers'],
                    "raw_text": htmlmin.minify(data['raw_text'].encode('utf-8').decode('utf-8'),
                                               remove_all_empty_space=True),
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
                    "query": "hufx6h5lcbcmpifa.onion"
                }
            }
        }
    }
    start_time = time.time()
    actions = []
    actions1 = []
    actions2 = []
    res = scan(client=es, query=search_query, scroll='50m', index='page', doc_type='_doc', timeout='1m')
    cnt = 0
    for record in res:
        print(cnt, record["_source"]["url"])
        cnt += 1
        html = record["_source"]["raw_text"]
        response = etree.HTML(html)

         #user
        if record["_source"]["url"][0:42] == 'http://hufx6h5lcbcmpifa.onion/home.php?mod':

            spider_name = 'onion_hufx6_bbs_spider'

            domain = 'hufx6h5lcbcmpifa.onion'

            net_type = 'tor'

            try:
                user_name = response.xpath('//h2[@class="mt"]/text()')[0].strip().replace('\\','')
            except:
                user_name = ''

            user_description = ''

            try:
                user_id = record["_source"]["url"]
                user_id = re.findall(r'uid=([\s|\S]+)', user_id)[0]
            except:
                user_id = ''

            try:
                url = record["_source"]["url"]
            except:
                url = ''

            try:
                raw_register_time = response.xpath('//ul[@id="pbbs"]/li[2]/text()')[0].strip()
            except:
                raw_register_time = ''

            try:
                register_time = datetime.strptime(raw_register_time, '%Y-%m-%d %H:%M')
                register_time = register_time - relativedelta(hours=8)
            except:
                register_time = None

            try:
                user_img_url = response.xpath('//div[@class="icn avt"]/a/img/@src')[0].strip()
            except:
                user_img_url = ''

            emails = email_extract(user_description)

            bitcoin_addresses = bitcoin_extract(user_description)

            eth_addresses = eth_extract(user_description)


            try:
                raw_last_active_time = response.xpath('//ul[@id="pbbs"]/li[3]/text()')[0].strip()
            except:
                raw_last_active_time = ''

            try:
                last_active_time = response.xpath('//ul[@id="pbbs"]/li[3]/text()')[0]
                last_active_time = datetime.strptime(last_active_time, '%Y-%m-%d %H:%M')
                last_active_time = last_active_time - relativedelta(hours=8)
            except:
                last_active_time = None

            area = ''

            try:
                ratings = response.xpath('//div[@id="psts"]/ul/li[3]/text()')[0].strip()
            except:
                ratings = ''

            try:
                level = response.xpath('//div[@id="psts"]/ul/li[2]/text()')[0].strip()
            except:
                level = ''

            member_degree = ''
            pgp = ''
            crawl_time = record["_source"]["crawl_time"]

            try:
                topic_nums = response.xpath('//ul[@class="cl bbda pbm mbm"]/li/a[3]/text()')[0]
                topic_nums = re.findall('(\d+)', topic_nums)[0]
            except:
                topic_nums = None

            goods_orders = None
            identity_tags = ''
            false = False

            id = sim_hash.u_id(spider_name,user_id)
            action = {
                "_index": 'user',
                "_type": '_doc',
                "_op_type": 'create',
                "_id":id,
                "_source": {
                    "spider_name": spider_name,
                    "domain": domain,
                    "net_type": net_type,
                    "user_name": user_name,
                    "user_description": user_description,
                    "user_id": user_id,
                    "url": url,
                    "raw_register_time":raw_register_time,
                    "register_time": register_time,
                    "user_img_url": user_img_url,
                    "emails": emails,
                    "bitcoin_addresses":bitcoin_addresses,
                    "eth_addresses":eth_addresses,
                    "raw_last_active_time": raw_last_active_time,
                    "last_active_time": last_active_time,
                    "area": area,
                    "ratings": ratings,
                    "level": level,
                    "member_degree": member_degree,
                    "pgp": pgp,
                    "crawl_time": crawl_time,
                    "topic_nums": topic_nums,
                    "goods_orders": goods_orders,
                    "identity_tags": identity_tags,
                    "is_portraited":false,
                    "is_analyzed":false,
                    "gmt_create": record["_source"]["gmt_create"],
                    "gmt_modified": record["_source"]["gmt_modified"],

                }
            }

            actions.append(action)
            success, _ = bulk(es, actions, index='user', raise_on_exception=False, raise_on_error=False)
            end_time = time.time()
            logger.info(end_time - start_time)

        # topic
        if record["_source"]["url"][0:54] == 'http://hufx6h5lcbcmpifa.onion/forum.php?mod=viewthread':

            spider_name = 'onion_hufx6_bbs_spider'

            domain = 'hufx6h5lcbcmpifa.onion'

            url = record["_source"]["url"]

            page_index_id = record["_id"]

            net_type = 'tor'

            topic_type = 'post'

            try:
                crawl_tags = []
                crawl = response.xpath('//div[@class="bm cl"]/div/a[4]/text()')
                for i in crawl:
                    c = i.replace('（密钥联系管理员admin）', '')
                    crawl_tags.append(c)
            except:
                crawl_tags = []

            try:
                title = response.xpath('//span[@id="thread_subject"][1]/text()')[0].strip()
            except:
                title = ''

            try:
                topic_id = record["_source"]["url"]
                topic_id = re.findall(r'tid=(.*?)&', topic_id)[0]
            except:
                topic_id = ''

            user_id = 'admin'

            user_name = 'admin'

            commented_user_id = ''

            comment_id = ''

            try:
                raw_content = response.xpath('//div[@id="postlist"]/div[1]')[0]
                raw_content = etree.tostring(raw_content, encoding='utf-8')
                raw_content = str(raw_content,encoding='utf-8')
            except:
                raw_content = ''

            try:
                content = response.xpath('//span[@id="thread_subject"][1]/text()')[0].strip()
            except:
                content = ''

            try:
                clicks_times = response.xpath('//span[@class="xi1"][1]/text()')[0]
                clicks_times = int(clicks_times)
            except:
                clicks_times = ''

            try:
                commented_times = response.xpath('//span[@class="xi1"][2]/text()')[0]
                commented_times = int(commented_times)
            except:
                commented_times = ''

            crawl_time = record["_source"]["crawl_time"]

            try:
                raw_publish_time = response.xpath('//div[@class="authi"][1]/em/text()')[0].replace('发表于 ', '')
            except:
                raw_publish_time = ''

            try:
                publish_time = datetime.strptime(raw_publish_time, '%Y-%m-%d %H:%M:%S')
                publish_time = publish_time - relativedelta(hours=8)
            except:
                publish_time = None

            try:
                thumbs_up = response.xpath('//span[@class="xi1"][2]/text()')[0]
                thumbs_up = int(thumbs_up)
            except:
                thumbs_up = None

            thumbs_down = None

            emails = email_extract(content)

            bitcoin_addresses = bitcoin_extract(content)

            eth_addresses = eth_extract(content)


            false = False

            id = sim_hash.t_id(spider_name,topic_id,user_id,raw_content,comment_id)
            action1 = {
                "_index": 'topic',
                "_type": '_doc',
                "_op_type": 'create',
                "_id":id,
                "_source": {
                    "spider_name":spider_name,
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
                    "publish_time":publish_time,
                    "raw_publish_time": raw_publish_time,
                    "thumbs_up": thumbs_up,
                    "thumbs_down": thumbs_down,
                    "emails": emails,
                    "bitcoin_addresses": bitcoin_addresses,
                    "eth_addresses": eth_addresses,
                    "is_extracted":false,
                    "is_analyzed":false,
                    "gmt_create": record["_source"]["gmt_create"],
                    "gmt_modified": record["_source"]["gmt_modified"],
                }
            }
            actions1.append(action1)
            success, _ = bulk(es, actions1, index='topic', raise_on_exception=False, raise_on_error=False)
            end_time = time.time()
            logger.info(end_time - start_time)

            p = response.xpath('//div[@id="postlist"]/div')
            if len(p) > 1:
                poster_list = response.xpath('//div[@id="postlist"]/div')  # 匹配多级div,发帖人和回帖人
                poster_lenght = len(poster_list)
                for index in range(1, poster_lenght):
                    poster = poster_list[index]

                    spider_name = 'onion_hufx6_bbs_spider'

                    domain = 'hufx6h5lcbcmpifa.onion'

                    url = record["_source"]["url"]

                    page_index_id = record["_id"]

                    net_type = 'tor'

                    topic_type = 'comment'

                    try:
                        crawl_tags = []
                        crawl = response.xpath('//div[@class="bm cl"]/div/a[4]/text()')
                        for i in crawl:
                            c = i.replace('（密钥联系管理员admin）', '')
                            crawl_tags.append(c)
                    except:
                        crawl_tags = []

                    try:
                        title = response.xpath('//span[@id="thread_subject"][1]/text()')[0].strip()
                    except:
                        title = ''

                    try:
                        topic_id = record["_source"]["url"]
                        topic_id = re.findall(r'tid=(.*?)&', topic_id)[0]
                    except:
                        topic_id = ''

                    try:
                        user_ids = poster.xpath('table/tbody/tr[1]/td[1]/div/div[1]/div/a/text()')
                        user_id = ''
                        for i in user_ids:
                            user_id += i
                    except:
                        user_id = ''

                    try:
                        user_names = poster.xpath('table/tbody/tr[1]/td[1]/div/div[1]/div/a/text()')
                        user_name = ''
                        for i in user_names:
                            user_name += i
                    except:
                        user_name = ''

                    commented_user_id = '1'

                    try:
                        comment_id = poster.xpath('table/tbody/tr[1]/td[1]/div/div[1]/div/a/@href')[0]
                        comment_id = re.findall(r'uid=([\s|\S]+)', comment_id)[0]
                    except:
                        comment_id = ''

                    try:
                        raw_content = etree.tostring(poster, encoding='utf-8')
                        raw_content = str(raw_content)
                    except:
                        raw_content = ''

                    try:
                        contents = poster.xpath(
                            'table/tr[1]/td[2]/div[2]/div/div[1]/table/tr/td/text()')
                        content = ""
                        for i in contents:
                            content += i + '\n'
                    except:
                        content = ''

                    clicks_times = None
                    commented_times = None
                    crawl_time = record["_source"]["crawl_time"]

                    try:
                        raw_publish_time = poster.xpath('table/tbody/tr[1]/td[2]/div[1]/div/div[2]/em/text()')[0].replace('发表于 ','')
                    except:
                        raw_publish_time = ''

                    try:
                        publish_time = datetime.strptime(raw_publish_time, '%Y-%m-%d %H:%M:%S')
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
                    action2 = {
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
                            "thumbs_up": thumbs_up,
                            "thumbs_down": thumbs_down,
                            "emails": emails,
                            "bitcoin_addresses": bitcoin_addresses,
                            "eth_addresses": eth_addresses,
                            "is_extracted": false,
                            "is_analyzed": false,
                            "gmt_create": record["_source"]["gmt_create"],
                            "gmt_modified": record["_source"]["gmt_modified"],
                        }
                    }
                    actions2.append(action2)
                    success, _ = bulk(es, actions2, index='topic', raise_on_exception=False, raise_on_error=False)
                    end_time = time.time()
                    logger.info(end_time - start_time)


if __name__ == '__main__':
    key()
