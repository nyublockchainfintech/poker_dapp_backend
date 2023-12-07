from fastapi.testclient import TestClient
from poker_dapp_backend.server.shuffle_main import app
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
