# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import re
import hashlib
import htmlmin
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline,FilesPipeline
from scrapy.pipelines.files import FSFilesStore,S3FilesStore,GCSFilesStore
from scrapy.utils.python import to_bytes
from Seaweedfs.stores import WeedFilesStore
from tor_spider.sim_hash import g_id,u_id,p_id,t_id

#下载图片 ImagesPipeline
class Agarth_DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['picture']:
                yield Request(url, meta={'item': item})
        except:
            pass


    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'goods'
        goods_id = re.findall(r'item/([\s|\S]+)', item['goods_id'])[0]
        spider_name = 'onion_agarth_market_spider'
        index_id = g_id(spider_name, goods_id)
        return './%s/%s/%s' % (index,index_id,image_guid)


class Agarth_DownloadImagesPipeline2(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['picture2']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'user'
        user_id = re.findall(r'vendor/([\s|\S]+)', item['user_id'])[0]
        spider_name = 'onion_agarth_market_spider'
        index_id = u_id(spider_name, user_id)
        return './%s/%s/%s' % (index,index_id,image_guid)


class Alibaba_DownloadImagesPipeline(ImagesPipeline):

    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['img']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'page'
        domain = 'alibaba2kw6qoh6o.onion'
        raw_text = htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)
        index_id = p_id(domain, raw_text)
        return './%s/%s/%s' % (index,index_id,image_guid)


class Apollo_DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['picture']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'goods'
        goods_id = re.findall(r'id=([\s|\S]+)', item['goods_id'])[0]
        spider_name = 'onion_apollo_market_spider'
        index_id = g_id(spider_name, goods_id)
        return './%s/%s/%s' % (index,index_id,image_guid)


class Apollo_DownloadImagesPipeline2(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['picture2']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'user'
        user_id = re.findall(r'id=([\s|\S]+)', item['user_id'])[0]
        spider_name = 'onion_apollo_market_spider'
        index_id = u_id(spider_name, user_id)
        return './%s/%s/%s' % (index,index_id,image_guid)

class Avenger_DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['picture']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'user'
        user_id = re.findall(r'user-(.*?).html', item['user_id'])[0]
        spider_name = 'onion_avenger_bbs_spider'
        index_id = u_id(spider_name, user_id)
        return './%s/%s/%s' % (index,index_id,image_guid)


class C2p3h_DownloadImagesPipeline(ImagesPipeline):

    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['img']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'page'
        domain = 'c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion'
        raw_text = htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)
        index_id = p_id(domain, raw_text)
        return './%s/%s/%s' % (index,index_id,image_guid)


class Cryptbbs_DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['picture']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'user'
        user_id = re.findall(r'uid=([\s|\S]+)', item['user_id'])[0]
        spider_name = 'onion_cryptbbs_bbs_spider'
        index_id = u_id(spider_name, user_id)
        return './%s/%s/%s' % (index,index_id,image_guid)


class Facebook_DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['img']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'page'
        domain = 'facebookcorewwwi.onion'
        raw_text = htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)
        index_id = p_id(domain, raw_text)
        return './%s/%s/%s' % (index, index_id, image_guid)

class Guns_DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['img']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'page'
        domain = 'gunsganjkiexjkew.onion'
        raw_text = htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)
        index_id = p_id(domain, raw_text)
        return './%s/%s/%s' % (index, index_id, image_guid)

class Gw6zz_DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['img']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'page'
        domain = 'gw6zzvqgy6v2czxrmphuerrtbirftvkyfkeoaiorg5qijqlsbqfpqjqd.onion'
        raw_text = htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)
        index_id = p_id(domain, raw_text)
        return './%s/%s/%s' % (index, index_id, image_guid)

class Horoio_DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['img']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'page'
        domain = 'horoiomuy6xignjv.onion'
        raw_text = htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)
        index_id = p_id(domain, raw_text)
        return './%s/%s/%s' % (index, index_id, image_guid)

class Hour24_DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['picture']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'goods'
        goods_id = re.findall('http://24hourspkcmd7bvr.onion/product/(.*?).html',item['goods_id'])[0]
        spider_name = 'onion_hour24_market_spider'
        index_id = g_id(spider_name, goods_id)
        return './%s/%s/%s' % (index,index_id,image_guid)


class Jesblog_DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['picture']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'topic'
        spider_name = 'onion_jesblog_blog_spider'
        topic_id = re.findall(r'stories/(.*?).html',item['topic_id'])[0]
        user_id = 'James Stanley'
        raw_content = item['raw_content']
        comment_id = ''
        index_id = t_id(spider_name, topic_id, user_id, raw_content, comment_id)
        return './%s/%s/%s' % (index,index_id,image_guid)


class Lfwpm_DownloadImagesPipeline(ImagesPipeline):

    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['img']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'page'
        domain = 'lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion'
        raw_text = htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)
        index_id = p_id(domain, raw_text)
        return './%s/%s/%s' % (index,index_id,image_guid)

class Ninan_DownloadImagesPipeline(ImagesPipeline):

    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['img']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'page'
        domain = 'ninanyykvluxfsba.onion'
        raw_text = htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)
        index_id = p_id(domain, raw_text)
        return './%s/%s/%s' % (index,index_id,image_guid)

class Nytime_DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['picture']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'topic'
        spider_name = 'onion_nytime_new_spider'
        topic_id = item['topic_id']
        user_id = item['user_id']
        raw_content = item['raw_content']
        comment_id = ''
        index_id = t_id(spider_name, topic_id, user_id, raw_content, comment_id)
        return './%s/%s/%s' % (index,index_id,image_guid)


class Pncld_DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['img']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'page'
        domain = 'pncldyerk4gqofhp.onion'
        raw_text = htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)
        index_id = p_id(domain, raw_text)
        return './%s/%s/%s' % (index,index_id,image_guid)


class Sfdu2_DownloadImagesPipeline(ImagesPipeline):

    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['img']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'page'
        domain = 'sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion'
        raw_text = htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)
        index_id = p_id(domain, raw_text)
        return './%s/%s/%s' % (index,index_id,image_guid)


class Shopt_DownloadImagesPipeline(ImagesPipeline):

    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['img']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'page'
        domain = 'shoptwgap2x3xbwy.onion'
        raw_text = htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)
        index_id = p_id(domain, raw_text)
        return './%s/%s/%s' % (index,index_id,image_guid)



class Torum_DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['img']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'page'
        domain = 'torum6uvof666pzw.onion'
        raw_text = htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'),remove_all_empty_space=True)
        index_id = p_id(domain, raw_text)
        return './%s/%s/%s' % (index,index_id,image_guid)


class Xs6qb_DownloadImagesPipeline(ImagesPipeline):
    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['picture']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'goods'
        goods_id = re.findall(r'tid=([\s|\S]+)', item['goods_id'])[0]
        spider_name = 'onion_xs6qb_market_spider'
        index_id = g_id(spider_name, goods_id)
        return './%s/%s/%s' % (index,index_id,image_guid)

class Yue4e_DownloadImagesPipeline(ImagesPipeline):

    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['img']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'page'
        domain = 'yue4eifx522t5zjb.onion'
        raw_text = htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)
        index_id = p_id(domain, raw_text)
        return './%s/%s/%s' % (index,index_id,image_guid)



class Zj4o7_DownloadImagesPipeline(ImagesPipeline):

    STORE_SCHEMES = {
        '':FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GCSFilesStore,
        'weed': WeedFilesStore
    }
    def get_media_requests(self,item,info):
        try:
            for url in item['img']:
                yield Request(url, meta={'item': item})
        except:
            pass

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        index = 'page'
        domain = '7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion'
        raw_text = htmlmin.minify(item['html'].encode('utf-8').decode('utf-8'), remove_all_empty_space=True)
        index_id = p_id(domain, raw_text)
        return './%s/%s/%s' % (index,index_id,image_guid)