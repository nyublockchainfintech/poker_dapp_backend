from dotenv import load_dotenv
import redis
import os

load_dotenv()

output = os.getenv("REDIS_HOST")


def connect_to_redis():
    """
    Connect to redis
    """
    REDIS_HOST = os.getenv("REDIS_HOST") or "localhost"
    return redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
