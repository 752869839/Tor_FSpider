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
from mylog import logger, exception_logger

logger = logger()

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
        start_time = time.time()
        actions = []
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
                        user_name = response.xpath('//h1[@class="gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl bp9cbjyn j83agx80"]/text()')[0]
                    except:
                        user_name = ''

                    user_description = ''

                    try:
                        user_id = response.xpath('//h1[@class="gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl bp9cbjyn j83agx80"]/text()')[0]
                    except:
                        user_id = ''

                    url = record["_source"]["url"]

                    raw_register_time = ''
                    register_time = None

                    try:
                        user_img_url = re.findall(
                            '<image style="height: 168px; width: 168px;" x="0" y="0" height="100%" preserveAspectRatio="xMidYMid slice" width="100%" xlink:href="(.*?)"></image>',
                            html)
                        user_img_url = [img.replace('amp;', '') for img in user_img_url]
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
                p = response.xpath('//div[@data-testid="Keycommand_wrapper_feed_story"]')
                if len(p) > 0:
                    poster_list = response.xpath(
                        '//div[@data-testid="Keycommand_wrapper_feed_story"]')
                    poster_lenght = len(poster_list)
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
                            topic_id = poster.xpath('div//div[@class="l9j0dhe7"]/@id')[0]
                        except:
                            topic_id = ''

                        try:
                            user_id = response.xpath('//h1[@class="gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl bp9cbjyn j83agx80"]/text()')[0]
                        except:
                            user_id = ''

                        try:
                            user_name = response.xpath('//h1[@class="gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl bp9cbjyn j83agx80"]/text()')[0]
                        except:
                            user_name = ''

                        commented_user_id = ''
                        comment_id = ''

                        try:
                            raw_content = poster.xpath('div//div[@class="l9j0dhe7"]')[0]
                            raw_content = etree.tostring(raw_content, encoding='utf-8')
                            raw_content = str(raw_content, encoding='utf-8')
                        except:
                            raw_content = ''

                        try:
                            contents = poster.xpath('div//div[@class="l9j0dhe7"]//text()')
                            content = ""
                            for i in contents:
                                content += i + '\n'
                        except:
                            content = ''

                        clicks_times = None
                        commented_times = None
                        crawl_time = record["_source"]["crawl_time"]

                        try:
                            raw_publish_time = poster.xpath(
                                'div//b[@class="b6zbclly myohyog2 l9j0dhe7 aenfhxwr l94mrbxd ihxqhq3m nc684nl6 t5a262vz sdhka5h4"]/text()')
                            raw_publish_time = [raw for raw in raw_publish_time if raw != "="][0]
                            print(type(raw_publish_time))

                            print(raw_publish_time)
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
                            thumbs_up = int(
                                poster.xpath('div//span[@class="gpro0wi8 cwj9ozl2 bzsjyuwj ja2t1vim"]//text()')[0])
                            print(thumbs_up)
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
                p = response.xpath('//div[@class="tw6a2znq sj5x9vvc d1544ag0 cxgpxx05"]')
                if len(p) > 0:
                    poster_list = response.xpath(
                        '//div[@class="tw6a2znq sj5x9vvc d1544ag0 cxgpxx05"]')
                    poster_lenght = len(poster_list)
                    print(poster_lenght)
                    for index in range(0, poster_lenght):
                        poster  = poster_list[index]

                        spider_name = 'onion_facebook_bbs_spider'

                        domain = 'facebookcorewwwi.onion'

                        net_type = 'tor'

                        try:
                            user_id = poster.xpath('div[@class="nc684nl6"]//text()')[0]
                        except:
                            user_id = ''

                        user_description = ''

                        try:
                            user_name = poster.xpath('div[@class="nc684nl6"]//text()')[0]
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
                p = response.xpath('//div[@data-testid="Keycommand_wrapper_feed_story"]')
                if len(p) > 0:
                    poster_list = response.xpath(
                        '//div[@data-testid="Keycommand_wrapper_feed_story"]')
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
                            topic_id = poster.xpath('div//div[@class="l9j0dhe7"]/@id')[0]
                        except:
                            topic_id = ''

                        try:
                            user_id = poster.xpath('div//div[@class="tw6a2znq sj5x9vvc d1544ag0 cxgpxx05"]/div[@class="nc684nl6"]//text()')[0]
                        except:
                            user_id = ''

                        try:
                            user_name = poster.xpath('div//div[@class="tw6a2znq sj5x9vvc d1544ag0 cxgpxx05"]/div[@class="nc684nl6"]//text()')[0]
                        except:
                            user_name = ''

                        try:
                            commented_user_id = response.xpath('//h1[@class="gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl bp9cbjyn j83agx80"]/text()')[0]
                        except:
                            commented_user_id = ''

                        try:
                            comment_id = poster.xpath('div//div[@class="tw6a2znq sj5x9vvc d1544ag0 cxgpxx05"]/div[@class="nc684nl6"]//text()')[0]
                        except:
                            comment_id = ''

                        try:
                            raw_content = poster.xpath('div//div[@class="tw6a2znq sj5x9vvc d1544ag0 cxgpxx05"]/div[@class="ecm0bbzt e5nlhep0 a8c37x1j"]')[0]
                            raw_content = etree.tostring(raw_content, encoding='utf-8')
                            raw_content = str(raw_content, encoding='utf-8')
                        except:
                            raw_content = ''

                        try:
                            contents = poster.xpath('div//div[@class="tw6a2znq sj5x9vvc d1544ag0 cxgpxx05"]/div[@class="ecm0bbzt e5nlhep0 a8c37x1j"]//text()')
                            content = ""
                            for i in contents:
                                content += i + '\n'
                        except:
                            content = ''

                        clicks_times = None
                        commented_times = None
                        crawl_time = record["_source"]["crawl_time"]

                        try:
                            raw_publish_time = poster.xpath('div//li[@class="_6coj"][last()]/a/span/text()')[0]
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
                        elif '天' in raw_publish_time:
                            t = raw_publish_time.replace('天 ', '')
                            day = int(re.findall('(.*?)天', raw_publish_time)[0])
                            yes = datetime.today() + timedelta(-day)
                            publish_time = yes.strftime('%Y-%m-%d %H:%M:%S')
                            publish_time = datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S')
                            publish_time = publish_time - relativedelta(hours=8)
                        elif '周' in raw_publish_time:
                            t = raw_publish_time.replace('周 ', '')
                            weekday = int(re.findall('(.*?)周', raw_publish_time)[0])
                            publish_time = datetime.today() - relativedelta(weeks=+weekday)
                            publish_time = publish_time.strftime('%Y-%m-%d %H:%M:%S')
                            publish_time = datetime.strptime(publish_time, '%Y-%m-%d %H:%M:%S')
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