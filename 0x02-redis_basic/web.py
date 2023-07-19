#!/usr/bin/env python3
"""
Redis as a http request rate counter
"""
import requests
import redis
import functools
from typing import Callable

redis_db = redis.Redis(host='127.0.0.1')


def count_requests(method: Callable) -> Callable:
    """
    A decorator function for counting how many times a request is made
    """
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        """
        count how many time a function is called and persis it in redis
        """
        key = "count:" + args[0]
        if redis_db.get(key) is None:
            redis_db.setex(key, 10, 1)
        redis_db.incr(key)
        return method(*args, **kwargs)
    return wrapper


@count_requests
def get_page(url: str) -> str:
    return requests.get(url).text
