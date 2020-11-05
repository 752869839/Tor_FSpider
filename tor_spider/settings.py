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

#proxy
HTTP_PROXY = ["http://172.16.30.66:3122","http://172.16.30.66:3124"]
SOCKS_PROXY = ['socks5://172.16.30.66:4759','socks5://172.16.30.66:4758']

#mysql
host="172.16.20.178"
port=3306
user="root"
password="root"
database='bjhgd'
table = 'bjhgd_tor_info'
cookie_table = 'bjhgd_account_info'
conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
# redis
REDIS_HOST = '172.16.20.178'
REDIS_PORT = '6379'
#seaweedfs
IMAGES_STORE =  'weed://172.16.20.178:8888/crawler'
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

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  # 使用scrapy_redis 里的去重组件，不使用scrapy默认的去重方式
SCHEDULER = "scrapy_redis.scheduler.Scheduler"  # 使用scrapy_redis 里的调度器组件，不使用默认的调度器
SCHEDULER_PERSIST = True    # 允许暂停，redis请求记录不丢失
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue' #使用优先级调度请求队列 （默认使用）
SCHEDULER_FLUSH_ON_START = True  # 自动清理redis里面的key

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

ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 100,
}

MEDIA_ALLOW_REDIRECTS = True    #因为图片地址会被重定向，所以这个属性要为True
# IMAGES_STORE =  './images'    #图片下载路径

COOKIES_ENABLED = True       #开启并使用自定义cookie中间件
# COOKIES_DEBUG =True        #跟踪cookiess

LOG_ENABLED = True       #开启日志
LOG_ENCODING = 'utf-8'  #日志字节码
LOG_LEVEL = 'INFO'      #日志级别
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
#AUTOTHROTTLE_START_DELAY = 5

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
