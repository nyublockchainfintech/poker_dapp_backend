from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from game import Game
from player import Player
import collections
from pydantic import BaseModel

#from poker_dapp_backend.server.dealer import Dealer

app = FastAPI()

connected_players = set()

curr_id = 1

rooms = collections.defaultdict(Game) #id:game

class PlayerModel(BaseModel):
    name: str
    balance: int
    hand: list
    status: int 
    
# TODO: Add join confirmation when a player joins the game
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     connected_players.add(websocket)
#     dealer = Dealer(connected_players)
#     try:
#         while True:
#             data = await websocket.receive_json()
#             print("Data received from a client:", data)
#             # Broadcast received data to all connected clients
#             await dealer.reply(data)
#     except WebSocketDisconnect:
#         connected_players.remove(websocket)
#         print(f"Client {websocket} disconnected")

@app.get("/ws/rooms/{game_id}")
async def get_game(game_id: int):
    return {  rooms[game_id].serialize() }

@app.get("/ws/all_rooms")
async def get_game():
    curr_games = ""

    for game_id, _ in rooms.items():
        curr_games += rooms[game_id].serialize()

    return {  curr_games }

@app.post("/ws/add_player")
async def add_player(player: PlayerModel):
    for game_id, game in rooms.items():
        if game.add_player(player.name, player.balance):
            rooms[game_id] = game
        else: 
            rooms[curr_id] = Game()
            rooms[curr_id].add_player(player.name, player.balance)
            curr_id += 1
    return player








