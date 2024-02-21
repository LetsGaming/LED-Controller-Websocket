import asyncio
import websockets
import json

async def client():
    uri = "ws://192.168.2.128:80"
    async with websockets.connect(uri) as websocket:
        # You are connected at this point. You can send/receive messages.
        while True:
            # Example: Receiving a message
            response = await websocket.recv()
            print(f"Received message: {response}")
            response_data = json.loads(response)
            if response_data["request"]:
                # Example: Sending a message
                message = {'status': 'success', 'response': True}
                await websocket.send(json.dumps(message))

# Run the client
asyncio.run(client())
