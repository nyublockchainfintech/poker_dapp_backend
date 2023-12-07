from typing import Dict
from poker_dapp_backend.contract.config import CONTRACT_ABI, RPC_URL, CONTRACT_ADDRESS
from poker_dapp_backend.server.utils import DictToObject
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from poker_dapp_backend.contract.connection import PokerGameTables
from poker_dapp_backend.server.game import Game
from pydantic import BaseModel
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
    game_table = PokerGameTables.connect_to_contract(
        RPC_URL, CONTRACT_ADDRESS, CONTRACT_ABI
    )
    try:
        while True:
            # Process incoming JSON message
            data = await websocket.receive_json()
            msg_type = data["MESSAGE_TYPE"]
            msg = data["MESSAGE"]

            # Assign players to rooms and store table metadata
            tables = game_table.get_all_tables()
            game_table.deserialize_all_tables(tables)

            # Find the game id for the player
            game_id = game_table.get_player_game_id(msg)
            # game_id = 0

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
                game_id = room_counter
                # NOTE: All this is is hard coded
                small_blind = 10
                big_blind = 20
                blinds = (10, 20)

                if rooms.get(game_id) is None:
                    rooms[game_id] = Game(
                        buy_in=msg["BUY_IN"],
                        blinds=blinds,
                    )
                    room_counter += 1
                    room_sockets[game_id] = []

                rooms[game_id].add_player(
                    msg["PLAYER_ADDRESS"],
                    msg["BALANCE"],
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
