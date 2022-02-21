# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import hashlib
import htmlmin
import logging
from scrapy import Request
from scrapy.utils.python import to_bytes
from scrapy.pipelines.images import ImagesPipeline,FilesPipeline
from scrapy.pipelines.files import FSFilesStore,S3FilesStore,GCSFilesStore
from seaweedfs.stores import WeedFilesStore
from tor_spider.sim_hash import es_id

logger = logging.getLogger(__name__)

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
            index_id = es_id(item["url"])
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
            index_id = es_id(item["url"])
            return './%s/%s/%s' % (index,index_id,image_guid)
        except Exception as e:
            pass