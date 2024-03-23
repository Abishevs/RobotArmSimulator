import asyncio
import websockets
import aioconsole

from commons.json_schema import validate_message

async def listen(websocket):
    try:
        async for message in websocket:
            print(f"Received: {message}")
    except websockets.ConnectionClosed:
        print("Connection closed by the server.")

async def send(websocket):
    while True:
        command = await aioconsole.ainput(">> ")
        await websocket.send(command)

async def main():
    uri = "ws://localhost:4203"
    async with websockets.connect(uri) as websocket:
        await asyncio.gather(
            listen(websocket),
            send(websocket),
        )

if __name__ == "__main__":
    position_update_message = {
    "messageType": "positionUpdate",
    "identifier": "123",
    "source": "arm",
    "target": "gui",
    "payload": {
        "positions": [
            {"jointId": 1, "currentAngle": 45},
            {"jointId": 2, "currentAngle": 90}
        ]
    }
}

    print(validate_message(position_update_message))
    asyncio.run(main())

