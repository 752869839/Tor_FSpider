### author LiZhi Chen

项目简介: 此项目为针对tor的暗网特定站点web数据采集、分析、存储
项目架构: tor通道 + scrapy + scrapyd + scrapydweb + mysql +  elasticsearch + seaweedfs + docker
环境依赖: 服务器n台操作系统不限、 docker版本不限、 mysql 5.7.32、 redis 6.0.8、 elasticsearch 7.8.1、 seaweedfs文件服务器、 tor通道n个

上传项目到目标服务器,系统防火墙需开放5000、6800、6801端口,并安装docker服务
cd /Tor_ASpider/docker
修改 scrapyd.conf、scrapyd_monitor.sh  相关配置为你部署服务器地址
docker build -t scrapyd:latest .      镜像构建时间可能较长耐心等待
将 /Tor_ASpider/docker/crontab.txt  内容输入crontab -e 设定定时任务
修改 /tor_spider/settings.py  相关配置


创建mapping
cd /docker/mapping  查看mapping说明按说明执行即可,ip修改为es地址即可
访问你部署ip:5000端口  x.x.x.x:5000 scrapydweb接口,将项目压缩.zip包或.rar包 上传运行即可

修改 /parse/config.py  相关配置
后台定期运行 /parse/launch.sh  执行特定爬虫数据解析
