#!/usr/bin/env python3
"""
Redis as a http request rate counter
"""
import requests
import redis
import functools
from typing import Callable

r = redis.Redis(host='127.0.0.1')


def url_access_count(method):
    """decorator for get_page function"""
    @functools.wraps(method)
    def wrapper(url):
        """wrapper function"""
        key = "cached:" + url
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

            # Get new content and update cache
        key_count = "count:" + url
        html_content = method(url)

        r.incr(key_count)
        r.set(key, html_content, ex=10)
        r.expire(key, 10)
        return html_content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """
    make a get request and return the value
    """
    return requests.get(url).text
