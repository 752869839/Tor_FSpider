# -*- coding: utf-8 -*-

# Scrapy settings for Agarth project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import pymysql
from datetime import datetime
from elasticsearch import Elasticsearch

#proxy
HTTP_PROXY = ["http://8.208.90.167:9398","http://8.208.15.45:9398"]
SOCKS_PROXY = ['socks5://47.242.73.94:29900','socks5://8.210.103.73:39901','socks5://198.11.182.140:29900','socks5://47.243.44.195:29900','socks5://47.254.41.41:29900','socks5://47.88.15.212:29900','socks5://8.210.121.248:29900']
# SOCKS_PROXY = ['socks5://172.16.30.66:8756','socks5://172.16.30.66:5791','socks5://172.16.30.66:7501','socks5://172.16.30.66:9976','socks5://172.16.30.66:6001','socks5://172.16.30.66:6002','socks5://172.16.30.66:6003','socks5://172.16.30.66:6004','socks5://172.16.30.66:6005','socks5://172.16.30.66:6006','socks5://172.16.30.66:6007','socks5://172.16.30.66:6008']

# elasticsearch
e_host='172.16.30.68'
e_port=9200
es_conn = Elasticsearch(hosts=e_host, port=e_port, timeout=30, max_retries=10)

#mysql
m_host="172.16.30.46"
m_port=3306
m_user="root"
m_password="root"
m_database='bjhgd'
p_database = 'hiddenmanage'
table = 'bjhgd_tor_info'
proxy_table = 'tunnel'
cookie_table = 'bjhgd_account_info'
mysql_conn = pymysql.connect(host=m_host, port=m_port, user=m_user, password=m_password, database=m_database)
proxy_mysql_conn = pymysql.connect(host=m_host, port=m_port, user=m_user, password=m_password, database=p_database)

# redis
REDIS_HOST = '172.16.30.45'
REDIS_PORT = '6379'

#seaweedfs
s_host='172.16.30.24'
s_port=8888
IMAGES_STORE =  f'weed://{s_host}:{s_port}/crawler'
ENABLE_IMAGE_SAVE = True
IMAGES_EXPIRES = 90

BOT_NAME = 'tor_spider'
SPIDER_MODULES = ['tor_spider.spiders']
NEWSPIDER_MODULE = 'tor_spider.spiders'
# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
DEFAULT_REQUEST_HEADERS = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Connection':'keep-alive',
'Upgrade-Insecure-Requests': '1' ,
}

ROBOTSTXT_OBEY = False

# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  # 使用scrapy_redis 里的去重组件，不使用scrapy默认的去重方式
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 使用scrapy_redis 里的调度器组件，不使用默认的调度器
# SCHEDULER_PERSIST = True    # 允许暂停，redis请求记录不丢失
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue' #使用优先级调度请求队列 （默认使用）
# SCHEDULER_FLUSH_ON_START = True  # 自动清理redis里面的key

# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline': 100,
# }

#可选用的其它队列
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'

# REDIS_PARAMS = {
#     # 'password': '',
#     'db': 0
# }

# # 去重队列的信息
# FILTER_URL = None
# FILTER_HOST = 'localhost'
# FILTER_PORT = 6379
# FILTER_DB = 0


MEDIA_ALLOW_REDIRECTS = True    #因为图片地址会被重定向，所以这个属性要为True
# IMAGES_STORE =  './images'    #图片下载路径

COOKIES_ENABLED = True       #开启并使用自定义cookie中间件
# COOKIES_DEBUG =True        #跟踪cookiess

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_LEVEL = 'INFO'
today = datetime.now()
log_file_path = "log/spiders-{}-{}-{}.log".format(today.year, today.month, today.day)
LOG_FORMAT='%(asctime)s [%(name)s] %(levelname)s: %(message)s'# 日志格式
LOG_DATEFORMAT='%Y-%m-%d %H:%M:%S'# 日志时间格式
#LOG_FILE = log_file_path    #日志保存为文件

USER_AGENT_TYPE = 'random'   #fake_useragent

#下载器中间件
DOWNLOADER_MIDDLEWARES = {
    'tor_spider.middlewares.IpProxyDownloadMiddleware': 300,
                    }
#爬虫中间件
#SPIDER_MIDDLEWARES = {
#    'AWS.middlewares.AwsSpiderMiddleware': 543,
#}
# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 0.01  #下载延时

# 初始下载延迟
AUTOTHROTTLE_START_DELAY = 2
# 在高延迟情况下设置的最大下载延迟
AUTOTHROTTLE_MAX_DELAY = 10

#使用RetryMiddleware中间件
RETRY_ENABLED = True
RETRY_TIMES = 3   #状态码重新请求数
RETRY_HTTP_CODES = [500, 503, 403, 404, 302]    #遇到这些状态码时候重新请求

# Scrapy downloader设置最大并发数（默认是16个，可以自己设置更多。但是要注意电脑的性能）
CONCURRENT_REQUESTS = 16

# 对单个网站进行并发请求的最大值。
CONCURRENT_REQUESTS_PER_DOMAIN = 16

# 对单个IP进行并发请求的最大值。如果非0,则忽略 CONCURRENT_REQUESTS_PER_DOMAIN 设定,使用该设定。
CONCURRENT_REQUESTS_PER_IP = 16

MYEXT_ENABLED=True      # 开启扩展
IDLE_NUMBER=300         # 配置空闲持续时间单位为 300个 ，一个时间单位为5s

# 在 EXTENSIONS 配置，激活扩展
EXTENSIONS= {
            'tor_spider.extensions.RedisSpiderSmartIdleClosedExensions': 500,
        }

#爬虫允许的最大深度，可以通过meta查看当前深度；0表示无深度
# DEPTH_LIMIT = 5

#0表示深度优先Lifo(默认)；1表示广度优先FiFo
# 后进先出，深度优先
# DEPTH_PRIORITY = 0
# SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleLifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.LifoMemoryQueue'
# 先进先出，广度优先

# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'