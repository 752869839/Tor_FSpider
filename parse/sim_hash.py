# -*- coding:utf-8 -*-
import re
import hashlib
from bs4 import BeautifulSoup
from simhash import Simhash



def simhash(s,width=3):
    """
    width:hash滑动步长
    s:待hash的输入
    """
    sim = s.strip()
    sim=re.sub('[ \n\t]','',sim)
    features = [sim[i:i + width] for i in range(max(len(sim) - width + 1, 1))]
    shash = Simhash(features)
    return shash


def p_id(domain,raw_text):

    """
    生成全网爬虫入库ID
    :param domain: 站点域名
    :param raw_text: 网页文本
    :return:
    """
    unlabel_text = ''.join(BeautifulSoup(raw_text, 'lxml').findAll(text=True))
    return str(simhash(domain+unlabel_text,3).value)



def t_id(spider_name,topic_id,user_id,raw_content,comment_id=''):
    """
    生成topic表数据入库ID
    :param spider_name: 爬虫节点名称
    :param topic_id: 话题ID
    :param user_id: 话题(评论)作者ID
    :param raw_content: 话题(评论)内容
    :param comment_id: 评论ID
    :return:
    """
    unlabel_text = ''.join(BeautifulSoup(raw_content, 'lxml').findAll(text=True))
    return hashlib.sha1((spider_name+topic_id+user_id+unlabel_text+comment_id).encode('utf-8')).hexdigest()


def u_id(spider_name,user_id):
    """
    生成user表数据入库ID
    :param spider_name: 爬虫节点名称
    :param user_id: 用户ID
    :return:
    """
    return hashlib.sha1((spider_name + user_id).encode('utf-8')).hexdigest()


def g_id(spider_name,goods_id):
    """
    生成goods表数据入库ID
    :param spider_name: 爬虫节点名称
    :param goods_id: 用户ID
    :return:
    """
    return hashlib.sha1((spider_name + goods_id).encode('utf-8')).hexdigest()





