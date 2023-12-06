from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from poker_dapp_backend.server.game import Game
from poker_dapp_backend.server.player import Player
import collections
from pydantic import BaseModel


app = FastAPI()

connected_players = set()
curr_games = ""

curr_id = 1

rooms = collections.defaultdict(Game)  # id:game

rooms = {1: Game(buy_in=20, blinds=[20, 30]), 2: Game(buy_in=10, blinds=[20, 30])}


class PlayerModel(BaseModel):
    name: str
    balance: int
    hand: list
    status: int




@app.get("/ws/rooms/{game_id}")
async def get_game(game_id: int):
    return {rooms[game_id].serialize()}


# @app.get("/ws/all_rooms")
# async def get_game():

#     for game_id, _ in rooms.items():
#         curr_games += rooms[game_id].serialize()

#     return {  curr_games }

# @app.post("/ws/add_player")
# async def add_player(player: PlayerModel):
#     for game_id, game in rooms.items():
#         if game.add_player(player.name, player.balance):
#             rooms[game_id] = game
#         else:
#             rooms[curr_id] = Game()
#             rooms[curr_id].add_player(player.name, player.balance)
#             curr_id += 1
#     return player
