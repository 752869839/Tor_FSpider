# -*- coding: utf-8 -*-
import time
from config import client,scrapyd


def scheduler_task():
    if  spider_name in scrapyd.list_spiders(project_name):
        scrapyd.schedule(project_name, spider_name)
        time.sleep(2)
        client.lpush("zj4o7:start_url", "http://7zj4oshsyhokgus6fyk7pmdiubu4mkjpjjprjkvopnhnwylr522tymqd.onion/user")

def select_jobs():
    scrapyd_dict = scrapyd.list_jobs(project_name)
    running_list = scrapyd_dict["running"]
    pending_list = scrapyd_dict["pending"]
    if len(running_list) >= 1 or len(pending_list) >= 1:
        for running_spider in running_list:
            job_id = running_spider["id"]
            scrapyd.cancel(project_name, job_id)


if __name__ == '__main__':
    project_name = 'tor_spider'
    spider_name = 'onion_zj4o7_market_spider'
    select_jobs()
    scheduler_task()



