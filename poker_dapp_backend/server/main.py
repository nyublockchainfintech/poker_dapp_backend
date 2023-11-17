from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

connected_clients = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print("Data received from a client:", data)
            # Broadcast received data to all connected clients
            await broadcast(data)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("A client disconnected")


async def broadcast(message: dict):
    disconnected_clients = set()
    for client in connected_clients:
        try:
            await client.send_json(message)
        except Exception:
            # If sending fails, assume client is disconnected
            disconnected_clients.add(client)
    # Remove disconnected clients
    for client in disconnected_clients:
        connected_clients.remove(client)
