### author LiZhi Chen

项目简介: 此项目为针对tor服务的onion地址站点 内容数据、图片数据 分布式采集、分析、存储
项目架构: tor协议通道 + scrapy_redis + scrapyd + scrapydweb + redis + mysql +  elasticsearch + seaweedfs + docker
环境依赖: 服务器n台操作系统不限、 docker版本不限、 mysql 5.7.32、 redis 6.0.8、 elasticsearch 7.8.1、 seaweedfs文件服务器、 tor通道n个

#(1)部署服务器(虚拟机)
上传项目包到目标服务器,系统防火墙需开放5000、6800端口 并安装docker服务
vim  /Tor_FSpider/docker/scrapyd_monitor.sh     修改相关配置为你部署机器ip
docker build -t scrapydcloud:latest .           镜像构建时间可能较长耐心等待
docker run -itd --restart=always --name=scrapydcloud -p 5000:5000 -p 6800:6800  -v /root/data:/root/data -h scrapydcloud -w /code scrapydcloud:latest /bin/bash  运行并启动容器
外部配置定时任务 crontab -e  配置内容为/Tor_FSpider/docker/crontab.txt中内容

#(2)创建mapping
vim /Tor_FSpider/schedule/mapping/extensive_mapping说明.txt  查看mapping说明 ip修改为es地址 按说明执行

#(3)浏览器访问
你部署ip:5000端口  http://x.x.x.x:5000/       scrapydweb出现代表部署成功
![image](https://user-images.githubusercontent.com/44913268/125924277-ed599b06-2c7c-46b0-b00c-524ca9e241ac.png)

#(4)浏览器所在桌面下修改相关配置(windows|mac) Tor_FSpider项目
修改文件  /Tor_FSpider/tor_spider/settings.py   相关配置
修改文件  /Tor_FSpider/schedule/config.py       相关配置
修改完毕后重新将Tor_FSpider 重新压缩成.zip或.rar的文件
选择 步骤3 scrapydweb中 Deploy Project选项下 Upload file  Select File 选择我们刚刚压缩过的文件后 Upload & Deploy
并 Run Spider 启动项目即可

#(5)任务下发 数据存储
运行/Tor_FSpider/schedule/lpush_task.py  推送任务到redis 采集任务即可获取到redis中待采集队列
找一台cpu高的机器后台运行 /Tor_FSpider/schedule/data_export.py  32进程数据从redis实时写入es

#分部署部署重复步骤(1)、(3)、(4)即可

