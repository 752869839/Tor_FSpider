# -*- coding: utf-8 -*-

from config import redis_client,mysql_conn


def getUrlFromDB():
    try:

        cur = mysql_conn.cursor()
        cur.execute("SELECT url FROM webservice WHERE `status`=1 and type='onion'")
        results = cur.fetchall()
        for domain in results:
            task_url = "http://" + domain[0]
            print(task_url)
            redis_client.lpush("whole", task_url)
        mysql_conn.commit()
        cur.close()
        mysql_conn.close()
    except Exception as e:
        print("Mysql Error %d:%s" % (e.args[0], e.args[1]))
        return None


if __name__ == '__main__':
    getUrlFromDB()