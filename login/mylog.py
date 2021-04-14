import os
import logging
import functools


def logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    fh = logging.StreamHandler()
    # fh = logging.FileHandler("{}/login/login.log".format(os.getcwd()))
    # fh = logging.FileHandler("{}/tor_spider/login/login.log".format(os.getcwd()))
    fmt = "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] - %(message)s"
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
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

