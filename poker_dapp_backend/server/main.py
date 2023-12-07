from typing import Dict
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from poker_dapp_backend.server.game import Game
import collections
from pydantic import BaseModel
from poker_dapp_backend.server.game import Game
import json


app = FastAPI()

connected_players = set()

rooms = {}

room_sockets = {}


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
            msg_type = data.get("MESSAGE_TYPE", None)
            msg = data.get("MESSAGE", None)
            game_id = msg.get("GAME_ID", None)
            
            # Process different message types
            if msg_type == "ACTION":
                player_index = rooms[game_id].get_player_index(msg["PLAYER NAME"])
                match msg["ACTION"]:
                    case "BET":
                        rooms[game_id].player_bet(player_index, msg["AMOUNT"])

                    case "CHECK":
                        rooms[game_id].player_check(player_index)

                    case "FOLD":
                        rooms[game_id].player_fold(player_index)

                    case _: 
                        raise ValueError("Invalid action")

            elif msg_type == "START_GAME":
                rooms[game_id].start_game()

            elif msg_type == "JOIN":
                rooms[game_id].add_player(
                    msg["PLAYER_NAME"],
                    msg["PLAYER_BALANCE"],
                )
                room_sockets[game_id].append(websocket)

            elif msg_type == "LEAVE":
                rooms[game_id].remove_player(msg["PLAYER_NAME"])
                room_sockets[game_id].remove(websocket)

            elif msg_type == "CREATE":
                game_id = room_counter
                small_blind = int(msg["BLINDS"][0])
                big_blind = int(msg["BLINDS"][1])
                blinds = (small_blind, big_blind)
                rooms[game_id] = Game(
                    buy_in=msg["BUY_IN"],
                    blinds=blinds,
                )
                room_counter += 1
                room_sockets[game_id] = []

            # Broadcast received data to all connected clients
            new_game_state = json.loads(rooms[game_id].serialize())
            for ws in room_sockets[game_id]:
                await ws.send_json(new_game_state)  # Modify as needed for broadcasting

    except WebSocketDisconnect:
        connected_players.remove(websocket)
        print(f"Client {websocket} disconnected")

