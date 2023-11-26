from fastapi.testclient import TestClient
from poker_dapp_backend.server.main import app  # Import your FastAPI app
from poker_dapp_backend.client.players import Player
from httpx import AsyncClient
import pytest
from contextlib import ExitStack

