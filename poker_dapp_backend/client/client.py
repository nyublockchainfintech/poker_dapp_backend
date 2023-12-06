# client.py
import asyncio
import websockets
from starlette.websockets import WebSocket
from poker_dapp_backend.client.players import ShufflePlayer
import json

TEST_URI = "ws://localhost:8000/ws"


async def connect():
    try:
        async with websockets.connect(TEST_URI) as websocket:
            player = ShufflePlayer(websocket)
            response = None
            while True:
                if response is None:
                    await websocket.send(json.dumps({"command": "join"}))
                else:
                    response = json.loads(response)
                    player.deserialize(response)
                    msg = player.reply()
                    await websocket.send(json.dumps(msg))
                response = await websocket.recv()
                print("Response from server:", response)
    except websockets.ConnectionClosedError as e:
        print(f"Connection closed unexpectedly: {e}")


asyncio.get_event_loop().run_until_complete(connect())
