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
    def wrapper(url):
        """
        count how many time a function is called and persis it in redis
        """
        count_key = "count:" + url
        redis_db.incr(count_key)

        result = method(url)

        cache_key = "cache:" + url
        if redis_db.get(cache_key) is None:
            redis_db.setex(cache_key, 10, result)
            return result
        return redis_db.get(cache_key).decode('utf-8')
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    make a get request and return the value
    """
    return requests.get(url).text
