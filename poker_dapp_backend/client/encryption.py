#encryption.py
import hashlib
import numpy as np
import binascii


def exor(v1, v2):
    a = np.frombuffer(v1, dtype=np.uint8)
    b = np.frombuffer(v2, dtype=np.uint8)
    re = (a ^ b).tobytes()
    return re


def symencrypt(key: bytes, message: bytes) -> bytes:
    """
    Encrypt a message using a password

    Args:
        key (bytes): Key to encrypt the message with
        message (bytes): Message to encrypt
    """
    user_key = hashlib.shake_128()
    user_key.update(key)
    key = user_key.digest(len(message))
    return exor(message, key)
