import pymysql

#proxy
PROXIES = [
    {"http": "108.61.203.227:9398"}
]


#mysql
host="172.16.30.46"
port=3306
user="root"
password="root"
database='bjhgd'
cookie_table = 'bjhgd_account_info'


conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database)


#自由国度账户
pncld_username = 'yuanxiao'     #yida    #ningmeng   #fengmi    #guazi     #kele   #shuibei   #shijin
#guoba    #xuebi    #pingguo   #jianpan    #baixiong   #tangyuan
pncld_word = 'Yanjingxianpi123456789'