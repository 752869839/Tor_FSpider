import os
import logging
from datetime import datetime

#日志
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter("[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] - %(message)s")
sh = logging.StreamHandler()
sh.setFormatter(formatter)
today = datetime.now()
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #上一级目录
log_file_path = path + "{}log{}login_monitoring-{}-{}-{}.log".format(os.sep, os.sep, today.year, today.month, today.day)
handler = logging.FileHandler(log_file_path, encoding='utf-8')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(sh)
