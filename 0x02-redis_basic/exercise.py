#!/usr/bin/env python3
"""
Writing strings to Redis 
"""
import sys
import redis
import uuid
from typing import Callable, Any, Optional, Union


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

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store key-value pair in redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[Any], Any]]):
        """
        retrieves key-value pair in redis
        """
        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def get_int(self: bytes) -> int:
        """convert to int"""
        return int.from_bytes(self, sys.byteorder)

    def get_str(self: bytes) -> str:
        """convert to string"""
        return self.decode("utf-8")
