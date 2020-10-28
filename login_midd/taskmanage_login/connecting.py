import pymysql
from login.config import host,port,user,password,database

# mysql连接
conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)