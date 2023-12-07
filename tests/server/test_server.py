import json
from poker_dapp_backend.server.utils import DictToObject


def test_shuffle_encrypt(server_create):
    ws1, p1_msg = server_create
    print(p1_msg)
    assert True
