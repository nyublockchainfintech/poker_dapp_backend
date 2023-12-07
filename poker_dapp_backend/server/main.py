from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from poker_dapp_backend.server.game import Game
from poker_dapp_backend.server.player import Player
import collections
from pydantic import BaseModel
from poker_dapp_backend.server.game import Game


# poetry run python3 -m uvicorn poker_dapp_backend.server.main:app


app = FastAPI()

connected_players = set()

rooms = collections.defaultdict(Game) #id:game

rooms = {1:Game(buy_in=20, blinds=[20, 30]), 2:Game(buy_in=10, blinds=[20, 30])}

    
class PlayerRoomModel(BaseModel):
    game_id: int
    name: str
    balance: int
    hand: list
    status: int 

class UpdateProfileModel(BaseModel):
    game_id: int
    old_name: str
    new_name: str


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
async def get_games():
    curr_games = ""

    for game_id, _ in rooms.items():
        curr_games += rooms[game_id].serialize()

    return {  curr_games }

@app.post("/ws/join_room")
async def join_room(player: PlayerRoomModel):
    # TODO CHECK REDIS IF NAME ALREADY EXISTS

    if len(rooms[player.game_id].players) == rooms[player.game_id].max_players:
        return { "Game is full, join another room" }

    else:
        rooms[player.game_id].add_player(player.name, player.balance)
        return { rooms[player.game_id].serialize() }

# TODO: Add game.remove()
@app.post("/ws/leave_room")
# async def leave_room(player: PlayerRoomModel):
#     rooms[player.game_id].remove(player.name)

#     return { rooms[player.game_id].serialize() } 

@app.post("/ws/update_profile")
async def update_profile(new_player: UpdateProfileModel):
    # TODO CHECK REDIS IF OLD NAME ALREADY EXISTS

    for player in rooms[new_player.game_id].players:
        if player.name == new_player.old_name:
            player.name = new_player.new_name

    return { rooms[new_player.game_id].serialize() } 
   

# class PlayerModel(BaseModel):
#     name: str
#     balance: int
#     hand: list
#     status: int 

# curr_id = 1

# Function to add player to whatever the open room is 
# @app.post("/ws/add_player")
# async def add_player(player: PlayerModel):
#     for game_id, game in rooms.items():
#         if game.add_player(player.name, player.balance):
#             rooms[game_id] = game
#         else: 
#             rooms[curr_id] = Game()
#             rooms[curr_id].add_player(player.name, player.balance)
#             curr_id += 1
#     return { player }