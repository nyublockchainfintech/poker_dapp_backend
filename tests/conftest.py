from fastapi.testclient import TestClient
from poker_dapp_backend.contract.connection import PokerGameTables
from poker_dapp_backend.contract.config import CONTRACT_ABI, RPC_URL, CONTRACT_ADDRESS
from poker_dapp_backend.server.shuffle_main import app
from poker_dapp_backend.server.main import app as main_app
from contextlib import ExitStack

import pytest


@pytest.fixture
def two_player_game():
    with ExitStack() as stack:
        client1 = TestClient(app)
        ws1 = stack.enter_context(client1.websocket_connect("/ws"))
        ws1.send_json({"command": "join"})
        p1_msg = ws1.receive_json()

        client2 = TestClient(app)
        ws2 = stack.enter_context(client2.websocket_connect("/ws"))
        ws2.send_json({"command": "join"})
        p2_msg = ws2.receive_json()

        yield ws1, ws2, p1_msg, p2_msg


@pytest.fixture
def server_create():
    with ExitStack() as stack:
        client1 = TestClient(main_app)
        ws1 = stack.enter_context(client1.websocket_connect("/ws"))
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

        yield ws1, p1_msg


@pytest.fixture
def contract_connection():
    return PokerGameTables.connect_to_contract(RPC_URL, CONTRACT_ADDRESS, CONTRACT_ABI)
