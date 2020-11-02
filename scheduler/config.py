from redis import StrictRedis
from scrapyd_api import ScrapydAPI

redis_host = '172.16.30.45'
# redis
client = StrictRedis(
    host=redis_host, port=6379, db=0
)

deploy_ip = '172.16.30.42'

scrapyd = ScrapydAPI('http://{}:6800'.format(deploy_ip))
