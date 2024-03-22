import asyncio
import websockets
import aioconsole

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
    asyncio.run(main())

