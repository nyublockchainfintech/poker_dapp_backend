from dotenv import load_dotenv
import json
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


class DictToObject:
    def __init__(self, data):
        self._attributes = {}
        for key, value in data.items():
            key = key.lower()
            if isinstance(value, dict):
                value = DictToObject(value)
            setattr(self, key, value)

    def __getattr__(self, name):
        # Return a default value for any attribute
        return self._attributes.get(name, "default value")

    def __setattr__(self, name, value):
        # Set the attribute in the internal dictionary
        if name == "_attributes":
            # This condition is necessary to initialize _attributes
            super().__setattr__(name, value)
        else:
            self._attributes[name] = value

    # serialize all the attributes
    def serialize(self):
        # recursively serialize nested objects
        for key, value in self._attributes.items():
            if isinstance(value, DictToObject):
                self._attributes[key] = value.serialize()
        return json.dumps(self._attributes)
