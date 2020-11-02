# -*- coding: utf-8 -*-
import re
import time
from lxml import etree
from datetime import datetime,timedelta
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
                        "query": "facebookcorewwwi.onion"
                    }
                }
            }
        }

        res = scan(client=es, query=search_query, scroll='1m', index='page', doc_type='_doc', timeout='1m')
        cnt = 0
        for record in res:
            print(cnt, record["_source"]["url"])
            cnt += 1
            html = record["_source"]["raw_text"]
            response = etree.HTML(html)
            try:
                # user
                if record["_source"]["url"][0:34] == 'https://www.facebookcorewwwi.onion':

                    spider_name = 'onion_facebook_bbs_spider'

                    domain = 'facebookcorewwwi.onion'

                    net_type = 'tor'

                    try:
                        user_name = response.xpath('//a[@class="_2nlw _2nlv"]/text()')[0]
                    except:
                        user_name = ''

                    user_description = ''

                    try:
                        user_id = response.xpath('//a[@class="_2nlw _2nlv"]/text()')[0]
                    except:
                        user_id = ''

                    url = record["_source"]["url"]

                    raw_register_time = ''
                    register_time = None

                    try:
                        user_img_url = response.xpath('//img[@class="_11kf img"]/@src')[0]
                    except:
                        user_img_url = ''

                    emails = email_extract(user_description)

                    bitcoin_addresses = bitcoin_extract(user_description)

                    eth_addresses = eth_extract(user_description)

                    raw_last_active_time = ''
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
                            #"last_active_time": last_active_time,
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
                p = response.xpath('//div[@id="timeline_story_column"]/div/div[@class="_5pcb _4b0l _2q8l"]')
                if len(p) > 0:
                    poster_list = response.xpath(
                        '//div[@id="timeline_story_column"]/div/div[@class="_5pcb _4b0l _2q8l"]')
                    poster_lenght = len(poster_list)
                    print(poster_lenght)
                    for index in range(0, poster_lenght):
                        poster = poster_list[index]

                        spider_name = 'onion_facebook_bbs_spider'

                        domain = 'facebookcorewwwi.onion'

                        url = record["_source"]["url"]

                        page_index_id = record["_id"]

                        net_type = 'tor'

                        topic_type = 'post'

                        crawl_tags = []
                        title = ''

                        try:
                            topic_id = poster.xpath('div/div/@id')[0]
                        except:
                            topic_id = ''

                        try:
                            user_id = response.xpath('//a[@class="_2nlw _2nlv"]/text()')[0]
                        except:
                            user_id = ''

                        try:
                            user_name = response.xpath('//a[@class="_2nlw _2nlv"]/text()')[0]
                        except:
                            user_name = ''

                        commented_user_id = ''
                        comment_id = ''

                        try:
                            raw_content = poster.xpath('div//div[@class="_1dwg _1w_m _q7o"]')[0]
                            raw_content = etree.tostring(raw_content, encoding='utf-8')
                            raw_content = str(raw_content, encoding='utf-8')
                        except:
                            raw_content = ''

                        try:
                            contents = poster.xpath('div//div[@class="_1dwg _1w_m _q7o"]//text()')
                            content = ""
                            for i in contents:
                                content += i + '\n'
                        except:
                            content = ''

                        clicks_times = None
                        commented_times = None
                        crawl_time = record["_source"]["crawl_time"]

                        try:
                            raw_publish_time = \
                            poster.xpath('div//span[@class="n_1kk0gpl5tm"]//span[@class="timestampContent"]/text()')[0]
                            raw_publish_time = str(raw_publish_time)
                        except:
                            raw_publish_time = ''

                        if '日' in raw_publish_time and '月' in raw_publish_time and '年' not in raw_publish_time and len(
                                    raw_publish_time) <= 6:
                            today = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                            year = re.findall('(.*?)-', today)[0]
                            p = datetime.strptime(raw_publish_time, '%m月%d日')
                            t = str(p).replace('1900', year)
                            publish_time = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
                            publish_time = publish_time - relativedelta(hours=8)
                        elif '日' in raw_publish_time and '月' in raw_publish_time and '年' in raw_publish_time:
                            publish_time = datetime.strptime(raw_publish_time, '%Y年%m月%d日')
                            publish_time = publish_time - relativedelta(hours=8)
                        elif '小时' in raw_publish_time:
                            hour = int(raw_publish_time.replace('小时', ''))
                            yes = datetime.today() - timedelta(hours=hour)
                            yesterday_format = yes.strftime('%Y-%m-%d %H:%M:%S')
                            publish_time = datetime.strptime(yesterday_format, '%Y-%m-%d %H:%M:%S')
                            publish_time = publish_time - relativedelta(hours=8)
                        elif '昨天' in raw_publish_time:
                            t = raw_publish_time.replace('昨天 ', '')
                            yes = datetime.today() + timedelta(-1)
                            yesterday_format = yes.strftime('%Y-%m-%d')
                            yesterday = datetime.strptime(yesterday_format, '%Y-%m-%d')
                            publish_time = str(yesterday).replace('00:00:00', t)
                            publish_time = datetime.strptime(publish_time, '%Y-%m-%d %H:%M')
                            publish_time = publish_time - relativedelta(hours=8)
                        elif '日' in raw_publish_time and '月' in raw_publish_time and ' ' in raw_publish_time:
                            today = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                            year = re.findall('(.*?)-', today)[0]
                            p = datetime.strptime(raw_publish_time, '%m月%d日 %H:%M')
                            t = str(p).replace('1900', year)
                            publish_time = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
                            publish_time = publish_time - relativedelta(hours=8)
                        else:
                            publish_time = None

                        try:
                            thumbs_up = int(poster.xpath('div//a[@class="_3dlf"]//text()')[0])
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
                                #"clicks_times": clicks_times,
                                #"commented_times": commented_times,
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



                #user
                p = response.xpath('//div[@id="timeline_story_column"]//ul[@class="_7791"]/li')
                if len(p) > 0:
                    poster_list = response.xpath(
                        '//div[@id="timeline_story_column"]//ul[@class="_7791"]/li')
                    poster_lenght = len(poster_list)
                    print(poster_lenght)
                    for index in range(0, poster_lenght):
                        poster = poster_list[index]

                        spider_name = 'onion_facebook_bbs_spider'

                        domain = 'facebookcorewwwi.onion'

                        net_type = 'tor'

                        try:
                            user_id = poster.xpath('div//a[@class="_6qw4"]/text()')[0]
                        except:
                            user_id = ''

                        user_description = ''

                        try:
                            user_name = poster.xpath('div//a[@class="_6qw4"]/text()')[0]
                        except:
                            user_name = ''

                        url = record["_source"]["url"]

                        raw_register_time = ''
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
                                # "register_time": register_time,
                                "user_img_url": user_img_url,
                                "emails": emails,
                                "bitcoin_addresses": bitcoin_addresses,
                                "eth_addresses": eth_addresses,
                                "raw_last_active_time": raw_last_active_time,
                                # "last_active_time": last_active_time,
                                "area": area,
                                "ratings": ratings,
                                "level": level,
                                "member_degree": member_degree,
                                "pgp": pgp,
                                "crawl_time": crawl_time,
                                # "topic_nums": topic_nums,
                                # "goods_orders": goods_orders,
                                "identity_tags": identity_tags,
                                "gmt_create": record["_source"]["gmt_create"],
                                "gmt_modified": record["_source"]["gmt_modified"],
                            }
                        }]
                        success, _ = bulk(es, actions, index='user', raise_on_exception=False, raise_on_error=False)

                # topic
                p = response.xpath('//div[@id="timeline_story_column"]/div/div[@class="_5pcb _4b0l _2q8l"]')
                if len(p) > 0:
                    poster_list = response.xpath(
                        '//div[@id="timeline_story_column"]/div/div[@class="_5pcb _4b0l _2q8l"]')
                    poster_lenght = len(poster_list)
                    print(poster_lenght)
                    for index in range(0, poster_lenght):
                        poster = poster_list[index]

                        spider_name = 'onion_facebook_bbs_spider'

                        domain = 'facebookcorewwwi.onion'

                        url = record["_source"]["url"]

                        page_index_id = record["_id"]

                        net_type = 'tor'

                        topic_type = 'comment'

                        crawl_tags = []
                        title = ''

                        try:
                            topic_id = poster.xpath('@id')[0]
                        except:
                            topic_id = ''

                        try:
                            user_id = poster.xpath('div//a[@class="_6qw4"]/text()')[0]
                        except:
                            user_id = ''

                        try:
                            user_name = poster.xpath('div//a[@class="_6qw4"]/text()')[0]
                        except:
                            user_name = ''

                        try:
                            commented_user_id = response.xpath('//a[@class="_2nlw _2nlv"]/text()')[0]
                        except:
                            commented_user_id = ''

                        try:
                            comment_id = poster.xpath('div//a[@class="_6qw4"]/@href')[0]
                            comment_id = re.findall('comment_id=([\s|\S]+)', comment_id)[0]
                        except:
                            comment_id = ''

                        try:
                            raw_content = poster.xpath('div//ul[@class="_7791"]/li/div')[0]
                            raw_content = etree.tostring(raw_content, encoding='utf-8')
                            raw_content = str(raw_content, encoding='utf-8')
                        except:
                            raw_content = ''

                        try:
                            contents = poster.xpath('div//ul[@class="_7791"]/li/div//text()')
                            content = ""
                            for i in contents:
                                content += i + '\n'
                        except:
                            content = ''

                        clicks_times = None
                        commented_times = None
                        crawl_time = record["_source"]["crawl_time"]

                        try:
                            raw_publish_time = poster.xpath('div//a[@class="_6qw7"]/abbr/@data-tooltip-content')[0]
                            raw_publish_time = str(raw_publish_time).replace('周一','').replace('周二','').replace('周三','').replace('周四','').replace('周五','').replace('周六','').replace('周日','')
                        except:
                            raw_publish_time = ''

                        try:
                            publish_time = datetime.strptime(raw_publish_time, '%Y年%m月%d日%H:%M')
                            publish_time = publish_time - relativedelta(hours=8)
                            print(publish_time)
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