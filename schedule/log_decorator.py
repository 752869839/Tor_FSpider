import os
import logging
import functools
from datetime import datetime

def _logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    today = datetime.now()
    path = os.path.dirname(os.path.abspath(__file__))  # 当前目录
    fh = logging.FileHandler(path + "{}log{}{}-{}-{}.log".format(os.sep, os.sep, today.year, today.month, today.day), encoding='utf-8')

    fmt = "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] - %(message)s"
    formatter = logging.Formatter(fmt)
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(sh)
    logger.addHandler(fh)
    return logger


def exception_logger(logger):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param logger: The logging object
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)

            # re-raise the exception
                raise

        return wrapper

    return decorator

