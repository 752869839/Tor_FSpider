from sfdu2 import Login
from connecting import re_queue
from com_log import logger

def login_tiem():
    freq = re_queue.exists('onion_sfdu2_market_spider:requests')
    logger.info(freq)
    if freq > 0:
        l = Login()
        l.main()


if __name__ == '__main__':
    login_tiem()
