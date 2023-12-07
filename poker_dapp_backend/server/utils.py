import redis


def connect_to_redis():
    """
    Connect to redis
    """
    return redis.Redis(host="localhost", port=6379, decode_responses=True)
