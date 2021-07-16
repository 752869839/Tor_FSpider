# -*- coding: utf-8 -*-
from config import redis_client


def lpush_url():
    with open('new_domain.txt', 'r', encoding='utf-8') as f:
        for domain in f:
            domain = domain.strip()
            if 'onion' in domain:
                task_url = "http://" + domain
                redis_client.lpush("whole", task_url)
        f.close()
    print('推送任务成功')

if __name__ == '__main__':
    lpush_url()
