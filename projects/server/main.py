import asyncio

from ws_server.ws_server import WebSocketServer

async def main():
    interval = 5
    server = WebSocketServer('0.0.0.0', 8000) 
    task1 = asyncio.create_task(server.run())
    task2 = asyncio.create_task(server.send_data_periodically(interval))
    await asyncio.gather(task1, task2)


if __name__ == "__main__":
    asyncio.run(main())
