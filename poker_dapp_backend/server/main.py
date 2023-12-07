from typing import Dict
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from poker_dapp_backend.server.game import Game
from poker_dapp_backend.server.player import Player
import collections
from pydantic import BaseModel
from poker_dapp_backend.server.game import Game


app = FastAPI()

connected_players = set()

rooms = {}


class PlayerRoomModel(BaseModel):
    game_id: int
    name: str
    balance: int
    hand: list
    status: int


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_players.add(websocket)
    room_counter = 0
    try:
        while True:
            data = await websocket.receive_json()
            msg = data.get("MESSAGE", None)
            game_id = msg.get("GAME_ID", None)

            # Process different message types
            if data["MESSAGE TYPE"] == "BET":
                rooms[game_id].bet(data["PLAYER ID"], data["AMOUNT"])

            elif data["MESSAGE TYPE"] == "JOIN":
                rooms[game_id].add_player(
                    msg["PLAYER NAME"],
                    msg["PLAYER BALANCE"],
                )

            elif data["MESSAGE TYPE"] == "CREATE":
                game_id = room_counter
                rooms[game_id] = Game(
                    buy_in=msg["BUY_IN"],
                    blinds=msg["BLINDS"],
                )
                room_counter += 1

            # Broadcast received data to all connected clients
            for ws in connected_players:
                await ws.send_json(data)  # Modify as needed for broadcasting

    except WebSocketDisconnect:
        connected_players.remove(websocket)
        print(f"Client {websocket} disconnected")
