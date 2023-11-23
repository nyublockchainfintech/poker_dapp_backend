# test_websockets.py
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from poker_dapp_backend.server.main import app  # Import your FastAPI app


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello world!")
        data = websocket.receive_json()
        print(data)
        assert data == {"msg": "Hello WebSocket"}
