import logging
import asyncio
import os

from dotenv import load_dotenv

from ws_server.ws_server import WebSocketServer
from commonlib.logger import setup_logging



async def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    load_dotenv()
    setup_logging(base_dir)

    ip = "0.0.0.0"
    port = 8000
    server = WebSocketServer(ip, port) 
    task1 = asyncio.create_task(server.run())
    logging.info("Application started")
    await asyncio.gather(task1)


if __name__ == "__main__":
    asyncio.run(main())
