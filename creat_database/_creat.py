# -*- coding: utf-8 -*-
import json
import pymysql
from datetime import datetime

"""
创建数据库,新建表并存储采集可配信息
project_name
domain 
proxy
username
password
gmt_create
"""

def set_up():
    try:
        conn = pymysql.connect(host="172.16.30.46", user="root", password="root")
        cursor = conn.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS %s' % 'basac')
        print("----创建库成功----")

        table_sql = """CREATE TABLE `tor_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(100) NOT NULL,
  `domain` varchar(500) NOT NULL ,
  `proxy` varchar(100) ,
  `username` varchar(100) ,
  `password` varchar(100) ,
  `gmt_create` datetime,
  PRIMARY KEY (`id`) USING BTREE
  ) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;
"""

        cursor.execute('use basac')
        try:
            cursor.execute(table_sql)
        except Exception as e:
            print(e)
        print("----创建表成功-----")

        data_sql = """insert  into `tor_info`(`id`,`project_name`,`domain`,`proxy`,`username`,`password`,`gmt_create`) values
(1,'tor_spider','c2p3hg35jalss7b2a6hkmhzflgevkonqt7g6jze62ro2g4h4wmzwobid.onion','{}','nongfu','shanquan','{}'),
(2,'tor_spider','xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion','{}','595341','ha12345','{}'),
(3,'tor_spider','xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion','{}','595343','ha12345','{}'),
(4,'tor_spider','7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion','{}','wahaha','laoganma','{}');
(5,'tor_spider','alibaba2kw6qoh6o.onion','{}','zuguo','laoganma','{}');
(6,'tor_spider','lfwpmgou2lz3jnt7mg3gorzkfnhnhgumbijn4ubossgs3wzsxkg6gvyd.onion','{}','nongfu','shanquan','{}');
(7,'tor_spider','pncldyerk4gqofhp.onion','{}','yuanxiao','Yanjingxianpi123456789','{}');
(8,'tor_spider','sfdu2jstlnp7whqlzpojopr5jxehxz4dveqfl67v6mfrwoj3nq6cnrad.onion','{}','bingning10','BINGNING','{}');
""".format(json.dumps(['http://8.208.90.167:9398', 'http://8.208.15.45:9398']),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),json.dumps(['http://8.208.90.167:9398', 'http://8.208.15.45:9398']),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),json.dumps(['http://8.208.90.167:9398', 'http://8.208.15.45:9398']),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),json.dumps(['http://8.208.90.167:9398', 'http://8.208.15.45:9398']),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),json.dumps(['http://8.208.90.167:9398', 'http://8.208.15.45:9398']),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),json.dumps(['http://8.208.90.167:9398', 'http://8.208.15.45:9398']),datetime.now().strftime("%Y-%m-%d %H:%M:%S"),json.dumps(['http://8.208.90.167:9398', 'http://8.208.15.45:9398']),datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(type(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        print(data_sql)
        cursor.execute(data_sql)
        print("----数据添加成功-----")
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    set_up()