# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import hashlib
import htmlmin
import logging
from lxml import etree
from scrapy import Request
from scrapy.utils.python import to_bytes
from scrapy.pipelines.images import ImagesPipeline,FilesPipeline
from scrapy.pipelines.files import FSFilesStore,S3FilesStore,GCSFilesStore
from elasticsearch.helpers import bulk
from seaweedfs.stores import WeedFilesStore
from tor_spider.sim_hash import p_id
from tor_spider.settings import es_conn
from tor_spider.extract_arithmetic import phone_extract,qq_extract,wechart_extract,alipay_extract,card_extract,tg_extract,pgp_extract,bitcoin_extract,eth_extract,email_extract

logger = logging.getLogger(__name__)
class TorWholeNetworkPipeline(object):
    def process_item(self, item, spider):
        response = etree.HTML(item['html'].encode('utf-8'))
        ele = response.xpath('//script | //noscript | //style')
        for e in ele:
            e.getparent().remove(e)
        index = 'extensive'
        actions = [{
            "_index": index,
            "_id": p_id(item['domain'],htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)),
            # "_type": '_doc',
            "_source": {
                "url": item['url'],
                "status": item['status'],
                "net_type": 'onion',
                "domain": item['domain'],
                "keywords": item['keywords'],
                "description": item['description'],
                "title": item['title'],
                "html": item['html'],
                "content": response.xpath("//html//body")[0].xpath("string(.)"),
                "language": item['language'],
                "encode": item['encode'],
                "significance": '',
                "category": [],
                "topic": [],
                "mirror": [],
                "phone_number": phone_extract(response.xpath("//html//body")[0].xpath("string(.)")),
                "qq": qq_extract(response.xpath("//html//body")[0].xpath("string(.)")),
                "wechat_id": wechart_extract(response.xpath("//html//body")[0].xpath("string(.)")),
                "alipay_id": alipay_extract(response.xpath("//html//body")[0].xpath("string(.)")),
                "card_id": card_extract(response.xpath("//html//body")[0].xpath("string(.)")),
                "telegram_id": tg_extract(response.xpath("//html//body")[0].xpath("string(.)")),
                "pgp": pgp_extract(response.xpath("//html//body")[0].xpath("string(.)")),
                "bitcoin_addresses": bitcoin_extract(response.xpath("//html//body")[0].xpath("string(.)")),
                "eth_addresses": eth_extract(response.xpath("//html//body")[0].xpath("string(.)")),
                "emails": email_extract(response.xpath("//html//body")[0].xpath("string(.)")),
                "crawl_time": item['crawl_time'],
                "gmt_create": item['crawl_time'],
                "gmt_modified": item['crawl_time'],
            }
        }]
        success, _ = bulk(es_conn, actions, index=index, raise_on_error=True)

        return item

class DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }

    def get_media_requests(self,item,info):
        try:
            for url in item['img_url']:
                yield Request(url, meta={'item': item}, )
        except:
            pass

    def file_path(self, request, response=None, info=None):
        try:
            item = request.meta['item']
            image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
            index = 'extensive'
            index_id = p_id(item["domain"], htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True))
            # logger.info(index_id)
            return './%s/%s/%s' % (index,index_id,image_guid)
        except Exception as e:
            logger.warning(e)


class DownloadfilesPipeline(FilesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }

    def get_media_requests(self, item, info):
        try:
            file = re.findall("magnet:\?xt=urn:btih:[A-za-z0-9]{40,40}[^\"]*", item["html"]) or re.findall("https://mega.nz/#![0-9A-Za-z]+![0-9A-Za-z]+", item["html"])
            for i in file:
                yield Request(i)
        except Exception as e:
            pass

    def file_path(self, request, response=None, info=None):
        try:
            item = request.meta['item']
            image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
            index = 'extensive_file'
            index_id = p_id(item["domain"], htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True))
            return './%s/%s/%s' % (index,index_id,image_guid)
        except Exception as e:
            pass