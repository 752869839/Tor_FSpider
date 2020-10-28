import redis
import pymysql
from config import host,port,user,password,database,r_host,r_port

# redis链接
re_queue = redis.Redis(host=r_host, port=r_port)

# mysql连接
conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)