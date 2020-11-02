# -*- coding: utf-8 -*-
import time
from config import client,scrapyd


def scheduler_task():
    if  spider_name in scrapyd.list_spiders(project_name):
        scrapyd.schedule(project_name, spider_name)
        time.sleep(2)
        client.lpush("shopt:start_url", "http://shoptwgap2x3xbwy.onion/")

def select_jobs():
    scrapyd_dict = scrapyd.list_jobs(project_name)
    running_list = scrapyd_dict["running"]
    pending_list = scrapyd_dict["pending"]
    if len(running_list) >= 1 or len(pending_list) >= 1:
        for running_spider in running_list:
            if running_spider["spider"] == spider_name:
                job_id = running_spider["id"]
                scrapyd.cancel(project_name, job_id)


if __name__ == '__main__':
    project_name = 'tor_spider'
    spider_name = 'onion_shopt_market_spider'
    select_jobs()
    scheduler_task()


