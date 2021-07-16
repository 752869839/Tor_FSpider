# -*- coding: utf-8 -*-

# Scrapy settings for tor_spider project
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
# SOCKS_PROXY = ['socks5://172.16.30.66:8756','socks5://172.16.30.66:5791','socks5://172.16.30.66:7501','socks5://172.16.30.66:9976','socks5://172.16.30.66:6001','socks5://172.16.30.66:6002','socks5://172.16.30.66:6003','socks5://172.16.30.66:6004','socks5://172.16.30.66:6005','socks5://172.16.30.66:6006','socks5://172.16.30.66:6007','socks5://172.16.30.66:6008']

# redis
REDIS_HOST = '172.16.30.45'
REDIS_PORT = '6379'
# REDIS_PARAMS = {
#     # 'password': '',
#     'db': 1
# }

# elasticsearch
e_host='172.16.30.68'
e_port=9200
es_conn = Elasticsearch(hosts=e_host, port=e_port, timeout=30,max_retries=10)

#mysql
m_host="172.16.30.46"
m_port=3306
m_user="root"
m_password="root"
p_database = 'hiddenmanage'
proxy_table = 'tunnel'
proxy_mysql_conn = pymysql.connect(host=m_host, port=m_port, user=m_user, password=m_password, database=p_database)

#seaweedfs
s_host='172.16.30.24'
s_port=8888
IMAGES_STORE =  f'weed://{s_host}:{s_port}/spider'
ENABLE_IMAGE_SAVE = True
IMAGES_EXPIRES = 90

BOT_NAME = 'tor_spider'

SPIDER_MODULES = ['tor_spider.spiders']
NEWSPIDER_MODULE = 'tor_spider.spiders'

#scrapy_redis
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  # 使用scrapy_redis 里的去重组件，不使用scrapy默认的去重方式
SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 使用scrapy_redis 里的调度器组件，不使用默认的调度器
SCHEDULER_PERSIST = True    # 允许暂停，redis请求记录不丢失
# SCHEDULER_FLUSH_ON_START = True  # 自动清理redis里面的key

# 使用优先级调度请求队列 （默认使用）
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
# 可选的 按先进先出排序（FIFO）
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'
# 可选的 按后进先出排序（LIFO）
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tor_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_LEVEL = 'INFO'
today = datetime.now()
log_file_path = "log/spiders-{}-{}-{}.log".format(today.year, today.month, today.day)
LOG_FORMAT='%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT='%Y-%m-%d %H:%M:%S'
#LOG_FILE = log_file_path    #日志保存为文件

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.1
DOWNLOAD_FAIL_ON_DATALOSS = False
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 3
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

#爬虫允许的最大深度，可以通过meta查看当前深度；0表示无深度
DEPTH_LIMIT = 7

#0表示深度优先Lifo(默认)；1表示广度优先FiFo
# 后进先出，深度优先
# DEPTH_PRIORITY = 0
# SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleLifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.LifoMemoryQueue'
# 先进先出，广度优先
# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

# MYEXT_ENABLED=True      # 开启扩展
IDLE_NUMBER=300         # 配置空闲持续时间单位为 300个 ，一个时间单位为5s

# 在 EXTENSIONS 配置，激活扩展
EXTENSIONS= {
            'tor_spider.extensions.RedisSpiderSmartIdleClosedExensions': 500,
        }

# DOWNLOAD_TIMEOUT = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
'Connection':'close',
'Upgrade-Insecure-Requests': '1',
}

USER_AGENT_TYPE = 'random'   #fake_useragent

# Enable or disable spider mi ddlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tor_spider.middlewares.TorWholeNetworkSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'tor_spider.middlewares.SocksProxyDownloadMiddleware': 156,
    'tor_spider.middlewares.StickyDepthSpiderMiddleware' : 101,
   # 'tor_spider.middlewares.RandomUserAgentMiddleware': 200,
   # 'tor_spider.middlewares.TorWholeNetworkDownloaderMiddleware': 543,
}

DOWNLOAD_HANDLERS = {
    'http': 'tor_spider.handlers.Socks5DownloadHandler',
    'https': 'tor_spider.handlers.Socks5DownloadHandler',
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 100,
   # 'tor_spider.pipelines.TorWholeNetworkPipeline': 355,
   # 'tor_spider.pipelines.DownloadImagesPipeline': 288,
}

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
