import json
from poker_dapp_backend.server.utils import DictToObject


def test_join(server_create):
    ws1 = server_create
    msg = {
        "MESSAGE_TYPE": "JOIN",
        "MESSAGE": {
            "PLAYER_ADDRESS": "0x3D4bDd0Daa396FA0b8B488FA7faF9050cb944239",
            "USERNAME": "test",
            "BALANCE": "100",
            "BUY_IN": "20",
            "BLINDS": ["10", "20"],
        },
    }
    ws1.send_json(msg)
    p1_msg = ws1.receive_json()
    print(p1_msg)
    assert True

