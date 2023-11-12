# server.py
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

app = FastAPI()

# A set to store active WebSocket connections
connected_clients = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Add the new connection to the set
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print("Data received from client:", data)
            # You can broadcast to all clients or handle each client individually
            for client in connected_clients:
                response = {"message": "Data received"}
                await client.send_json(response)
    except WebSocketDisconnect:
        # Remove the client from the set when it disconnects
        connected_clients.remove(websocket)
        print("Client disconnected")
