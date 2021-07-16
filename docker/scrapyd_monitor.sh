#!/bin/bash

ip=172.16.20.179
port=6800

spider_names='
onion_tor_whole_spider
'
project_name=tor_whole_network
deploy_name=tor

scrapyd_process=`ps aux |grep -E '/usr/local/bin/scrapyd$' |grep python3`
if [ -z "$scrapyd_process" ];then
        echo scrapyd dead
        nohup scrapyd  > /root/scriapyd_monitor.log 2>&1 &
        #sleep 5
        #for spider_name in $spider_names;do
                #cd /code/$project_name
                #scrapyd-deploy $deploy_name -p $project_name

                #params="-d project=$project_name -d spider=$deploy_name"

                #curl http://$ip:$port/schedule.json -d project=$project_name -d spider=$spider_name
        done
else
        echo "scrapyd is running"
fi

scrapydweb_process=`ps aux |grep -E '/usr/local/bin/scrapydweb$' |grep python3`
if [ -z "$scrapydweb_process" ];then
	echo scrapydweb dead
	nohup scrapydweb  > /root/scriapydweb_monitor.log 2>&1 &
else
	echo "scrapyd is running"
fi

