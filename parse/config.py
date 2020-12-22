import pymysql
from redis import StrictRedis
from elasticsearch6 import Elasticsearch

#redis
r_host='172.16.20.178'
r_port=6379
db=0

# elasticsearch
e_host='172.16.20.178'
e_port=9200


# mysql
m_host = '172.16.20.178'
m_port = 3306
user = 'root'
password = 'root'
database = 'bjhgd'
table = 'bjhgd_pyname_info'

#seaweedfs
sea_host = '172.16.20.178'
sea_port = 8888

# redis
client = StrictRedis(host=r_host, port=r_port, db=db)

# elasticsearch
es = Elasticsearch(hosts=e_host, port=e_port)

# mysql
conn = pymysql.connect(host=m_host, port=m_port, user=user, password=password, database=database)
