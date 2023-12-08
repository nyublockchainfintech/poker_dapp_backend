import json
from poker_dapp_backend.server.utils import DictToObject


def test_two_player_join(two_player_poker_game):
    ws1, ws2 = two_player_poker_game
    p1_msg = {
        "MESSAGE_TYPE": "JOIN",
        "MESSAGE": {
            "PLAYER_ADDRESS": "0x3D4bDd0Daa396FA0b8B488FA7faF9050cb944239",
            "USERNAME": "player 1",
            "BALANCE": "100",
            "BUY_IN": "20",
        },
    }
    ws1.send_json(p1_msg)
    p1_reply = ws1.receive_json()
    p2_msg = {
        "MESSAGE_TYPE": "JOIN",
        "MESSAGE": {
            "PLAYER_ADDRESS": "0x7F1eC556De6F68822Bf8D3b3E5Bf8A7Cbb533F21",
            "USERNAME": "player 2",
            "BALANCE": "100",
            "BUY_IN": "20",
        },
    }
    ws2.send_json(p2_msg)
    p2_reply = ws2.receive_json()
    assert len(p1_reply["players"]) == 1
    assert len(p2_reply["players"]) == 2


def test_two_player_bet(two_player_poker_game):
    ws1, ws2 = two_player_poker_game
    p1_msg = {
        "MESSAGE_TYPE": "JOIN",
        "MESSAGE": {
            "PLAYER_ADDRESS": "0x3D4bDd0Daa396FA0b8B488FA7faF9050cb944239",
            "USERNAME": "player 1",
            "BALANCE": "100",
            "BUY_IN": "20",
        },
    }
    ws1.send_json(p1_msg)
    p1_reply = ws1.receive_json()
    p2_msg = {
        "MESSAGE_TYPE": "JOIN",
        "MESSAGE": {
            "PLAYER_ADDRESS": "0x7F1eC556De6F68822Bf8D3b3E5Bf8A7Cbb533F21",
            "USERNAME": "player 2",
            "BALANCE": "100",
            "BUY_IN": "20",
        },
    }
    ws2.send_json(p2_msg)
    p2_reply = ws2.receive_json()
    assert len(p1_reply["players"]) == 1
    assert len(p2_reply["players"]) == 2
