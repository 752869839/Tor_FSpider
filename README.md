### author LiZhi Chen

项目简介: 此项目为针对tor服务的onion特定站点、明网网络安全相关站点 内容数据、图片数据 采集、分析、存储
项目架构: tor协议通道 + scrapy + scrapyd + scrapydweb + redis + mysql +  elasticsearch + seaweedfs + docker
环境依赖: 服务器n台操作系统不限、 docker版本不限、 mysql 5.7.32、 redis 6.0.8、 elasticsearch 7.8.1、 seaweedfs文件服务器、 tor通道n个、 国外socks代理n个

#(1)部署服务器(虚拟机)
上传项目包到目标服务器,系统防火墙需开放5000、6800端口 并安装docker服务
vim  /Tor_ASpider/docker/scrapyd_monitor.sh     修改相关配置为你部署机器ip
docker build -t scrapydcloud:latest .           镜像构建时间可能较长耐心等待
docker run -itd --restart=always --name=scrapydcloud -p 5000:5000 -p 6800:6800  -v /root/data:/root/data -h scrapydcloud -w /code scrapydcloud:latest /bin/bash  运行并启动容器
外部配置定时任务 crontab -e  配置内容为/Tor_FSpider/docker/crontab.txt中内容

#(2)创建mapping
vim /Tor_ASpider/docker/mapping/disignated_mapping说明.txt  查看mapping说明 ip修改为es地址 按说明执行

#(3)浏览器访问
你部署ip:5000端口  http://x.x.x.x:5000/       scrapydweb出现代表部署成功
![image](https://user-images.githubusercontent.com/44913268/122175026-dc93ac80-ceb5-11eb-91a7-5e3760c3bb0f.png)

#(4)修改配置 启动任务
浏览器所在桌面下修改(windows|mac) Tor_FSpider下
修改文件  /Tor_ASpider/tor_spider/settings.py   相关配置
修改文件  /Tor_ASpider/login/config.py          相关配置
修改文件  /Tor_ASpider/parse/config.py          相关配置
修改完毕后重新将Tor_ASpider 重新压缩成.zip或.rar的文件
选择 步骤3 scrapydweb中 Deploy Project选项下 Upload file  Select File 选择我们刚刚压缩过的文件后 Upload & Deploy
并 Run Spider 选择启动特定目标任务

#(5)数据解析 数据存储
后台定期运行 /Tor_ASpider/parse/launch.sh  执行特定爬虫数据解析

