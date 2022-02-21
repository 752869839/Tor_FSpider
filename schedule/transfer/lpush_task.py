# -*- coding: utf-8 -*-
from config import redis_client


def lpush_url():
    with open('new_v3.txt', 'r', encoding='utf-8') as f:
        for task_url in f:
            task_url = task_url.strip()
            if 'http' not in task_url:
                task_url = "http://" + task_url
            print(task_url)
            redis_client.lpush("whole", task_url)
    print('推送任务成功')

if __name__ == '__main__':
    lpush_url()
