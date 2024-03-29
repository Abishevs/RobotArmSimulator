import asyncio
import websockets
import json
from random import randint

async def send_initial_identity(websocket, identifier):
    initial_message = {
        "messageType": "positionUpdate",
        "identifier": identifier,
    }
    await websocket.send(json.dumps(initial_message))
    print(f"Sent initial identity: {identifier}")

async def listen_for_new_identity(websocket):
    try:
        response = await websocket.recv()
        print(f"Received: {response}")
        response_data = json.loads(response)
        return response_data.get("identifier")
    except websockets.ConnectionClosed:
        print("Connection closed by the server.")
        return None

async def main():
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        # Step 1: Send initial identity to the server
        await send_initial_identity(websocket, "gui")
        
        # Step 2: Wait for the server's response with a new identity
        new_identifier = await listen_for_new_identity(websocket)
        print(f"Assigned new identifier: {new_identifier}")

        # Now, use the new_identifier for further communication
        while True:
            # one = int(input("1: "))
            # two = int(input("2: "))
            # three = int(input("3: "))
            one = randint(0,180)
            two = randint(0,180)
            three = randint(0,180)
            position_update_message = {
                "messageType": "positionUpdate",
                "identifier": new_identifier,  # Use the new identifier from the server
                "payload": {
                    "positions": [
                        {"jointId": 1, "currentAngle": one},
                        {"jointId": 2, "currentAngle": two},
                        {"jointId": 3, "currentAngle": three}
                    ]
                }
            }
            await websocket.send(json.dumps(position_update_message))
            print(f"Sent position update with {new_identifier}")
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())

