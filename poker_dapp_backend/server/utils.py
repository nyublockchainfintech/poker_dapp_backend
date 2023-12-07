import redis
from dotenv import load_dotenv
import os

load_dotenv()


def connect_to_redis():
    """
    Connect to redis
    """
    REDIS_HOST = "redisdb"
    return redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
