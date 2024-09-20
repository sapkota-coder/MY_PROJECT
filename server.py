import asyncio
import websockets
import os
from colorama import Fore, Style
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

FILE_PATH = r'C:\Users\RADHE RADHE\Desktop\New folder (2)\input.txt'

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, websocket_manager):
        self.websocket_manager = websocket_manager

    def on_modified(self, event):
        if event.src_path == FILE_PATH:
            with open(FILE_PATH, 'r') as file:
                content = file.read()
            asyncio.run(self.websocket_manager.broadcast(content))

class WebSocketManager:
    def __init__(self):
        self.connected = set()

    async def register(self, websocket):
        self.connected.add(websocket)
        # Send the current content of the file to the newly connected client
        with open(FILE_PATH, 'r') as file:
            content = file.read()
        await websocket.send(content)

    async def unregister(self, websocket):
        self.connected.remove(websocket)

    async def broadcast(self, message):
        for websocket in self.connected:
            try:
                await websocket.send(message)
            except:
                self.connected.remove(websocket)

async def handler(websocket, path):
    await websocket_manager.register(websocket)
    try:
        async for _ in websocket:
            pass
    finally:
        await websocket_manager.unregister(websocket)

async def main():
    event_handler = FileChangeHandler(websocket_manager)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(FILE_PATH), recursive=False)
    observer.start()

    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # Run forever
print(f"{Fore.GREEN}server running........{Style.RESET_ALL  }")
if __name__ == "__main__":
    websocket_manager = WebSocketManager()
    asyncio.run(main())
