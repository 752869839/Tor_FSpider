#!/bin/bash

ip=172.16.30.42
port=6800

spider_names='
onion_agarth_market_spider
onion_alibaba_market_spider
onion_apollo_market_spider
onion_avenger_bbs_spider
onion_c2p3h_market_spider
onion_cryptbbs_bbs_spider
onion_guns_market_spider
onion_gw6zz_market_spider
onion_horoio_blog_spider
onion_hour24_market_spider
onion_jesblog_blog_spider
onion_lfwpm_bbs_spider
onion_ninan_market_spider
onion_nytime_new_spider
onion_pncld_bbs_spider
onion_sfdu2_market_spider
onion_shopt_market_spider
onion_torum_bbs_spider
onion_xs6qb_market_spider
onion_yue4e_market_spider
onion_zj4o7_market_spider
'
project_name=tor_spider
deploy_name=tor

scrapyd_process=`ps aux |grep /usr/local/bin/scrapyd|grep python3`
if [ -z "$scrapyd_process" ];then
        echo scrapyd dead
        nohup scrapyd  > /root/scriapyd_monitor.log 2>&1 &
        sleep 5
        for spider_name in $spider_names;do
                cd /code/$project_name
                scrapyd-deploy $deploy_name -p $project_name

                params="-d project=$project_name -d spider=$deploy_name"

                curl http://$ip:$port/schedule.json -d project=$project_name -d spider=$spider_name
        done
else
        echo "scrapyd is running"
fi
