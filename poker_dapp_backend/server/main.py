from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from poker_dapp_backend.server.dealer import Dealer

app = FastAPI()

connected_players = set()


@app.websocket("/shuffle")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_players.add(websocket)
    dealer = Dealer(connected_players)
    try:
        while True:
            data = await websocket.receive_json()
            print("Data received from a client:", data)
            # Broadcast received data to all connected clients
            await dealer.reply(data)
    except WebSocketDisconnect:
        connected_players.remove(websocket)
        print("A client disconnected")
