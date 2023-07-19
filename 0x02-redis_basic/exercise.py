#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import functools
import re
import redis
import uuid
from typing import Callable, Any, Optional, Union


def count_calls(method: Callable) -> Callable:
    """
    A decorator function for counting how many times a method is called
    """
    key = method.__qualname__

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        count how many time a function is called and persis it in redis
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    store the history of inputs and outputs for a particular function.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        store the history of inputs and outputs for a particular function.
        """
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        self._redis.rpush(input_key, str(args))
        return_value = method(self, *args, **kwargs)
        self._redis.rpush(output_key, return_value)

        return return_value
    return wrapper


def replay(method: Callable):
    """
    display the history of calls of a particular function.
    """
    redis_db = redis.Redis(host='127.0.0.1')

    method_name = method.__qualname__

    print(method_name + " was called " +
          redis_db.get(method_name).decode("utf-8") + " times:")

    all_keys = redis_db.keys()
    args = redis_db.lrange(method_name+":inputs", 0, -1)
    for arg in args:
        data_key = None
        str_arg = arg.decode("utf-8")
        for key in all_keys:
            key_str = key.decode('utf-8')
            value = None
            try:
                value = redis_db.get(key_str).decode("utf8")
            except Exception:
                pass
            find = re.findall(r'[\d]+', str_arg)
            if value == str_arg[2:-3]:
                data_key = key_str

            if len(find) > 0 and str(find[0]) == value:
                data_key = key_str

        print("{}(*{}) -> {}".format(method_name, str_arg, data_key))


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

    @call_history
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


cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)
replay(cache.store)
