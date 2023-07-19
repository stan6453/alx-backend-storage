#!/usr/bin/env python3
"""
Writing strings to Redis
"""
from functools import wraps
import redis
import uuid
from typing import Callable, Any, Optional, Union


def count_calls(method: Callable) -> Callable:
    """
    a system to count how many
    times methods of the Cache class are called.
    :param method:
    :return:
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrap
        :param self:
        :param args:
        :param kwargs:
        :return:
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache():
    """
    Cache class
    """

    def __init__(self) -> None:
        """
        Initialize Redis db connection
        """
        self._redis = redis.Redis(host='127.0.0.1')
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store key-value pair in redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Optional[Callable[[bytes], Any]] = None
    ) -> Union[str, bytes, int, float, None]:
        """
        retrieves key-value pair in redis
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Union[str, None]:
        """
        get a string from redis store
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        get an int from redis store
        """
        return self.get(key, fn=lambda d: int(d))
