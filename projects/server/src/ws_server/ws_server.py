import logging
import asyncio
import json
from typing import Dict, Optional, Set

from websockets.exceptions import ConnectionClosed
from websockets.legacy.server import WebSocketServerProtocol
from websockets.server import serve

from commonlib.json_schema import validate_message
from commonlib.enums import (Identifier, MessageType)

# Setup module level logger
logger = logging.getLogger(__name__)


class Client:
    """Represent a connected websocket client"""

    def __init__(self, websocket: WebSocketServerProtocol) -> None:
        super().__init__()
        self.websocket: WebSocketServerProtocol = websocket
        self._identifier: Optional[Identifier] = None  # e.g. GUI, MANAGED
        self._message_type: Optional[MessageType] = None
        self.source: Optional[str] = None
        self.target: Optional[str] = None
        self.paylod: Optional[Dict] = None

    @property
    def message_type(self):
        if self._message_type is None:
            logger.error("No message type present")
            raise ValueError("No message type present")
        return self._message_type

    @message_type.setter
    def message_type(self, value: str | MessageType):
        if isinstance(value, MessageType):
            self._message_type = value

        elif isinstance(value, str):
            try:
                self._message_type = MessageType(value)
            except ValueError:
                logger.error(f"Invalid identifier: {value}")
                raise ValueError(f"Invalid identifier: {value}")
        else:
            logger.error(f"Doesnt support type: {type(value)}")
            raise TypeError(f"Doesnt support type: {type(value)}")

    @property
    def identifier(self):
        if self._identifier is None:
            logger.error("No identifier present")
            raise ValueError("No identifier present")
        return self._identifier

    @identifier.setter
    def identifier(self, value: str | Identifier):
        if isinstance(value, Identifier):
            self._identifier = value

        elif isinstance(value, str):
            try:
                self._identifier = Identifier(value)
            except ValueError:
                logger.error(f"Invalid identifier: {value}")
                raise ValueError(f"Invalid identifier: {value}")
        else:
            logger.error(f"Doesnt support type: {type(value)}")
            raise TypeError(f"Doesnt support type: {type(value)}")

    def create_header(self):
        header = {"messageType": self.message_type.value,
                  "identifier": self.identifier.value,
                  }
        return header

    def create_json_res(self, payload: Dict):
        """constructs header and payload
        Returns: json string
        """
        data = {}
        data.update(self.create_header())
        data["payload"] = payload
        return json.dumps(data)

    def __str__(self) -> str:
        return f"Client(identifier: {self.identifier}, messageType: {self.message_type})"


class RobotArmStateManager:
    def __init__(self) -> None:
        self.state: Optional[Dict] = {}  # Holds payload updatePostion
        self.controller_client: Optional[Client] = None
        self.managed_client: Optional[Client] = None
        self.viewer_clients: Set[Client] = set()

    def add_client(self, websocket: WebSocketServerProtocol, msg_data) -> str:
        """
        Gets header json and sets as
        either controller, managed or viewer client.
        Send back clients new role.

         Returns: (str) *json string
        """
        client = Client(websocket)
        client.message_type = msg_data.get("messageType")
        client.identifier = msg_data.get("identifier")

        if not self.controller_client and client.identifier == Identifier.GUI:
            self.controller_client = client
            client.identifier = Identifier.CONTROLLER
            logger.info("Controller GUI connected")

        elif not self.managed_client and client.identifier == Identifier.MANAGED:
            # IRL robotic Arm to be managed by controller client
            self.managed_client = client
            logger.info("Managed client connected")

        elif client.identifier == Identifier.GUI:
            # viewer/broadcast clients
            client.identifier = Identifier.VIEWER
            self.viewer_clients.add(client)
            logger.info("Viewer GUI connected")

        else:
            raise ValueError("Unexpected websocket")

        logger.debug(client)

        data = client.create_header()
        return json.dumps(data)

    def disconnect_client(self, websocket: WebSocketServerProtocol):
        client = self.get_client(websocket)

        if client == self.controller_client:
            self.controller_client = None
            logger.info("Controller GUI disconnected")

        elif client == self.managed_client:
            self.managed_client = None
            logger.info("Managed client disconnected")

        elif client in self.viewer_clients:
            self.viewer_clients.remove(client)
            logger.info("Viewer client disconnected")

    def get_client(self, websocket):
        """Internal method to get client and its identifier"""
        if self.controller_client and self.controller_client.websocket == websocket:
            return self.controller_client

        if self.managed_client and self.managed_client.websocket == websocket:
            return self.managed_client

        for viewer_client in self.viewer_clients:
            if viewer_client.websocket == websocket:
                return viewer_client

        raise ValueError("Unknown websocket client")


class WebSocketServer:
    def __init__(self,
                 host: str,
                 port: int) -> None:
        self.host = host
        self.port = port
        self.state_manager: RobotArmStateManager = RobotArmStateManager()

    async def handler(self, websocket: WebSocketServerProtocol):
        try:
            # handle initial message/ first message
            init_msg = await websocket.recv()
            init_msg_data = json.loads(init_msg)
            validate_message(init_msg_data)

            # For state manegment
            res = self.state_manager.add_client(websocket, init_msg_data)
            validate_message(json.loads(res))
            await websocket.send(res)

            # Handle next messages
            async for msg in websocket:
                msg_data = json.loads(msg)
                validate_message(msg_data)

                await self.process_message(websocket, msg_data)
                print(f'recieved: {msg}')

        except ConnectionClosed:
            logger.info("A client has disconnected.")

        except Exception:
            logger.exception("Unexpected error occured")

        finally:
            self.state_manager.disconnect_client(websocket)

    async def process_message(self,
                              websocket: WebSocketServerProtocol,
                              msg_data: Dict) -> None:
        client = self.state_manager.get_client(websocket)
        if client.identifier == Identifier.CONTROLLER:
            # await self.state_manager.managed_client.websocket.send(json.dumps(msg_data))
            if msg_data["messageType"] == MessageType.POSITIONUPDATE.value:
                self.state_manager.state = msg_data.get("payload")
                data = json.dumps(msg_data)

                # forward to managed client and broadcast to viewers
                if not self.state_manager.managed_client:
                    # No IRL connected
                    logger.error("Managed client not connected")
                    # Send this back to controller
                    return

                await self.state_manager.managed_client.websocket.send(data)
                logger.info("Send new positins to managed client")

                for viewer in self.state_manager.viewer_clients:
                    await viewer.websocket.send(data)

        elif client.identifier == Identifier.MANAGED:
            # Updates from Managed client
            if msg_data["messageType"] == MessageType.POSITIONUPDATE.value:
                self.state_manager.state = msg_data.get("payload")
                data = {"messageType": MessageType.POSITIONUPDATE.value,
                        "payload": self.state_manager.state
                        }
                if not self.state_manager.controller_client:
                    logger.info("No GUI connected")
                    return

                await self.state_manager.controller_client.websocket.send(json.dumps(data))
                for viewer in self.state_manager.viewer_clients:
                    await viewer.websocket.send(json.dumps(data))
                logger.info("Broadcasting initial position updates")

        elif client.identifier == Identifier.VIEWER:
            pass

    async def run(self):
        async with serve(self.handler, self.host, self.port):
            await asyncio.Future()
