# -*- coding: utf-8 -*-
import time
import datetime
from functools import wraps


def timestamp():
    """时间戳"""
    return time.time()


def time_to_str(dt, fmt="%Y-%m-%d %H:%M:%S"):
    return dt.strftime(fmt)


def dt_strftime(fmt="%Y%m%d%H%M%S"):
    """
    datetime格式化时间
    :param fmt "%Y%m%d %H%M%S \ %Y-%m-%d %H:%M:%S.%f
    """
    return datetime.datetime.now().strftime(fmt)


def sleep(seconds=1.0):
    """
    睡眠时间
    """
    time.sleep(seconds)


def running_time(func):
    """函数运行时间"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = timestamp()
        res = func(*args, **kwargs)
        print("请求耗时%.3f秒！" % (timestamp() - start))
        return res

    return wrapper


if __name__ == '__main__':
    print(dt_strftime("%Y%m%d%H%M%S%f"))
