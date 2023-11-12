# client.py
import asyncio
import websockets
import json


async def connect():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        data = {"message": "Hello Server!"}
        await websocket.send(json.dumps(data))
        response = await websocket.recv()
        print("Response from server:", response)


asyncio.get_event_loop().run_until_complete(connect())
