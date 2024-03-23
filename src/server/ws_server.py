import asyncio
import json
from random import randint
from websockets.exceptions import ConnectionClosed
from websockets.server import serve

from commons.logger import LoggerConfig as Log
from commons.json_schema import validate_message

class WebSocketServer:
    def __init__(self, 
                 host: str,
                 port: int) -> None:
        self.host = host
        self.port = port
        self.connected_clients: set = set()

    async def handler(self, websocket, path):
        self.connected_clients.add(websocket)
        Log.info(f"Connected to client: {websocket}")
        try:
            async for msg in websocket:
                # if msg == "Move":
                    # res = f"{randint(-90, 90)}" 
                    # await websocket.send(f"Moved {res} degrees")
                msg_data = json.loads(msg)
                print(f'recieved: {msg_data}')
                await websocket.send(f'echo {msg}')
        except ConnectionClosed:
            Log.info("A client has disconnected.")
        finally:
            self.connected_clients.remove(websocket)

    async def run(self):
        async with serve(self.handler, self.host, self.port):
            Log.info(f"Server started at ws://{self.host}:{self.port}")
            await asyncio.Future()

    async def send_data_periodically(self, interval):
        """Send data to all connected clients at the specified interval."""
        while True:
            # Wait for the specified interval
            await asyncio.sleep(interval)
            # Prepare the data to be sent
            data = f"Periodic data: {randint(-90, 90)}" 
            # Send data to all connected clients
            for client in self.connected_clients:
                await client.send(data)
                Log.info(f"Sent data to client: {data}")

async def main():
    interval = 5
    server = WebSocketServer('localhost', 4203) 
    task1 = asyncio.create_task(server.run())
    task2 = asyncio.create_task(server.send_data_periodically(interval))
    await asyncio.gather(task1, task2)


if __name__ == "__main__":
    asyncio.run(main())

# asyncio.run(main())
