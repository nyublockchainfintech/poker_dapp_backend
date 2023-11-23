# client.py
import asyncio
import websockets
from starlette.websockets import WebSocket
from poker_dapp_backend.client.players import Player
import json


async def connect():
    uri = "ws://localhost:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            player = Player(websocket)
            response = None
            while True:
                # message = input("Enter a message (y/n): ")
                # if message == "n":
                #     await websocket.send(json.dumps({"command": "disconnect"}))
                #     break
                # elif message == "y":
                if response is not None:
                    try:
                        response = json.loads(response)
                        await player.reply(response)
                    except json.JSONDecodeError:
                        print("Invalid JSON")
                        continue
                else:
                    await websocket.send(json.dumps({"command": "join"}))
                # else:
                #     print("Invalid input")
                #     continue

                response = await websocket.recv()
                print("Response from server:", response)
    except websockets.ConnectionClosedError as e:
        print(f"Connection closed unexpectedly: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


asyncio.get_event_loop().run_until_complete(connect())
