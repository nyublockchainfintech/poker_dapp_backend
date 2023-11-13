import libnum
import sys
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


# TODO: Move some of the following code to a test file
if __name__ == "__main__":
    M = b"hello"
    key1 = b"bobpass"
    key2 = b"alicepass"

    # Encrypt the message with key1, then key2
    print("Message: ", M.decode())

    cipher1 = symencrypt(key1, M)
    cipher2 = symencrypt(key2, cipher1)

    print("Bob's key applied: ", binascii.hexlify(cipher1).decode())
    print("Alice's key applied: ", binascii.hexlify(cipher2).decode())

    # Decrypt the message with key2, then key1
    print("\nDecrypting with Alice's key, then Bob's")
    cipher3 = symencrypt(key2, cipher2)
    cipher4 = symencrypt(key1, cipher3)

    print("Message: ", cipher4.decode())
