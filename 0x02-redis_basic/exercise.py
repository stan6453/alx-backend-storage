#!/usr/bin/env python3
"""
Writing strings to Redis 
"""
import redis
import uuid
from typing import Callable, Any, Optional


class Cache():
    """
    Cache class
    """

    def __init__(self) -> None:
        """
        Initialize Redis db connection 
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: str | bytes | int | float) -> str:
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
        result = self._redis.get(key)
        if fn is None:
            return result
        return fn(result)
