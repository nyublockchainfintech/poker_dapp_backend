# client.py
import asyncio
import websockets
import json


async def connect():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        # Run an infinite loop to stay connected
        while True:
            # Listen for user input
            message = input("Enter a message (y/n): ")
            if message == "y":
                # Send a disconnect message to the server (optional)
                await websocket.send(json.dumps({"command": "disconnect"}))
                break
            else:
                # TODO: Modify this to send correct message to the server
                await websocket.send(json.dumps({"message": message}))

            # Wait for server response
            response = await websocket.recv()
            # TODO: Process the response from the server
            print("Response from server:", response)


asyncio.get_event_loop().run_until_complete(connect())
