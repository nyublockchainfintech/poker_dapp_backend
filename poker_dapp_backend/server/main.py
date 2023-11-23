from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from poker_dapp_backend.server.dealer import Dealer

app = FastAPI()

connected_players = set()


# NOTE: Use this connection manager soon
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


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
