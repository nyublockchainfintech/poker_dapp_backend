from fastapi.testclient import TestClient
from poker_dapp_backend.server.main import app  # Import your FastAPI app
from contextlib import ExitStack

import pytest


@pytest.fixture
def two_player_game():
    with ExitStack() as stack:
        client1 = TestClient(app)
        websocket1 = stack.enter_context(client1.websocket_connect("/ws"))
        websocket1.send_json({"command": "join"})
        data1 = websocket1.receive_json()

        client2 = TestClient(app)
        websocket2 = stack.enter_context(client2.websocket_connect("/ws"))
        websocket2.send_json({"command": "join"})
        data2 = websocket2.receive_json()

        yield websocket1, websocket2, data1, data2
