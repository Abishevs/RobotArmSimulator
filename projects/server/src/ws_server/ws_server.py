import asyncio
import json
from random import randint
from typing import Dict, Optional, Set

from websockets.exceptions import ConnectionClosed
from websockets.legacy.server import WebSocketServerProtocol
from websockets.server import serve

from commonlib.logger import LoggerConfig as Log
from commonlib.json_schema import validate_message

class RobotArmStateManager:
    def __init__(self) -> None:
        self.state: Optional[Dict] = {} # Holds parsed json state

class WebSocketServer:
    def __init__(self, 
                 host: str,
                 port: int) -> None:
        self.host = host
        self.port = port
        self.controller_client: Optional[WebSocketServerProtocol] = None
        self.connected_clients: set = set()
        self.viewer_clients: Set[WebSocketServerProtocol] = set()

    async def handler(self, websocket, path):
        if self.controller_client is None:
            self.controller_client = websocket
        else:
            self.connected_clients.add(websocket)
        Log.info(f"Connected to client: {websocket}")
        try:
            async for msg in websocket:
                # if msg == "Move":
                    # res = f"{randint(-90, 90)}" 
                    # await websocket.send(f"Moved {res} degrees")
                msg_data = json.loads(msg)
                await self.process_message(websocket, msg_data)
                print(f'recieved: {msg_data}')
                # await websocket.send(f'echo {res}')

        except ConnectionClosed:
            Log.info("A client has disconnected.")
        finally:
            if websocket == self.controller_client:
                self.controller_client = None
            else:
                self.connected_clients.remove(websocket)

    async def process_message(self, websocket: WebSocketServerProtocol, msg_data: Dict):
        msg_type = msg_data.get('messageType')
        print(f"rec msg_type: {msg_type}")
        if msg_type == "positionUpdate":
            if self.is_controlling_client(websocket):
                print("Is the controller")
                await websocket.send("YOOO controller")
            else:
                await websocket.send("BREE just a viewer")

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

    def is_controlling_client(self, websocket: WebSocketServerProtocol) -> bool:
        return websocket == self.controller_client
