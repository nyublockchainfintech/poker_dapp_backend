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

rooms = collections.defaultdict(Game)  # id:game

rooms = {1: Game(buy_in=20, blinds=[20, 30]), 2: Game(buy_in=10, blinds=[20, 30])}

# rooms = {1:Game(buy_in=20, blinds=[20, 30]), 2:Game(buy_in=10, blinds=[20, 30])}

    
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
    try:
        while True:
            data = await websocket.receive_json()
            game_id = data["MESSAGE"]["GAME ID"]
            # Process different message types
            if data["MESSAGE TYPE"] == "BET":
                rooms[game_id].bet(data["PLAYER ID"], data["AMOUNT"])

            elif data["MESSAGE TYPE"] == "JOIN":
                rooms[game_id].add_player(data["MESSAGE"]["PLAYER NAME"], data["MESSAGE"]["PLAYER BALANCE"])

            elif data["MESSAGE TYPE"] == "CREATE":
                rooms[game_id] = Game(buy_in=data["MESSAGE"]["BUY IN"], blinds=data["MESSAGE"]["BLINDS"])

            # Broadcast received data to all connected clients
            for ws in connected_players:
                await ws.send_json(data)  # Modify as needed for broadcasting

    except WebSocketDisconnect:
        connected_players.remove(websocket)
        print(f"Client {websocket} disconnected")

@app.post("/ws/start_game/{game_id}")
async def start_game(game_id: int):
    if game_id not in rooms:
        return {"error": "Game not found"}

    game = rooms[game_id]
    if not game.start_game():
        return {"error": "Cannot start game"}

    return {"message": "Game started", "game_state": game.serialize()}

#create a new game
@app.get("/ws/new_game/{buy_in}/{small_blind}/{big_blind}")
async def new_game(buy_in: int, small_blind: int, big_blind: int):
    global curr_id
    rooms[curr_id] = Game(buy_in=buy_in, blinds=[small_blind, big_blind])
    curr_id += 1
    return {"message": "Game created", "game_id": curr_id - 1}

@app.get("/ws/rooms/{game_id}")
async def get_game(game_id: int):
    return {rooms[game_id].serialize()}


 
@app.get("/ws/all_rooms")
async def get_game():
    global curr_games
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








