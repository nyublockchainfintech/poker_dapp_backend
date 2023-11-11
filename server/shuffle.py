import libnum
import sys
import hashlib
import numpy as np
import binascii


def xor_two_str(a, b):
    return "".join(
        [
            hex(ord(a[i % len(a)]) ^ ord(b[i % (len(b))]))[2:]
            for i in range(max(len(a), len(b)))
        ]
    )


M = b"hello"
p1 = b"bobpass"
p2 = b"alicepass"
ty = "SHAKE128"


def exor(v1, v2):
    a = np.frombuffer(v1, dtype=np.uint8)
    b = np.frombuffer(v2, dtype=np.uint8)
    re = (a ^ b).tobytes()
    return re


if len(sys.argv) > 1:
    M = str(sys.argv[1]).encode()
if len(sys.argv) > 2:
    p1 = str(sys.argv[2]).encode()
if len(sys.argv) > 3:
    p2 = str(sys.argv[3]).encode()
if len(sys.argv) > 4:
    ty = str(sys.argv[4])

if ty == "SHAKE128":
    print("Using SHAKE128")
    key_bob = hashlib.shake_128()
    key_bob.update(p1)
    key_alice = hashlib.shake_128()
    key_alice.update(p2)
else:
    print("Using SHAKE256")
    key_bob = hashlib.shake_256()
    key_bob.update(p1)
    key_alice = hashlib.shake_256()
    key_alice.update(p2)

print("Message: ", M.decode())

print("\nBob key stream: \t", binascii.hexlify(key_bob.digest(len(M))).decode())
print("Alice key stream:\t", binascii.hexlify(key_alice.digest(len(M))).decode())

print("\nApplying Bob Key and then Alice")
c1 = exor(M, key_bob.digest(len(M)))
c2 = exor(c1, key_alice.digest(len(M)))

print("Bob's key applied:\t", binascii.hexlify(c1).decode())
print("Alice's key applied:\t", binascii.hexlify(c2).decode())

print("\nRemoving Bob Key and then Alice")
c3 = exor(c2, key_bob.digest(len(M)))
m = exor(c3, key_alice.digest(len(M)))

print("After Bob's key applied:\t", binascii.hexlify(c3).decode())
print("After Alice's key applied:\t", m.decode())
