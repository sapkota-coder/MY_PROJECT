import asyncio
import websockets
from colorama import Fore, Style

WEB_SOCKET_URL = 'ws://localhost:8765'
OUTPUT_FILE_PATH = r'C:\Users\RADHE RADHE\Desktop\New folder (2)\saved_data.txt'

while True:
    async def save_data_to_file():
        try:
            async with websockets.connect(WEB_SOCKET_URL) as websocket:
                async for message in websocket:
                    with open(OUTPUT_FILE_PATH, 'w') as file:
                        file.write(message)
                    print(f"{Fore.GREEN}Data received and saved to {OUTPUT_FILE_PATH}{Style.RESET_ALL}")
        except Exception as E:
            print(f"{Fore.RED} {E} {Style.RESET_ALL}")
    if __name__ == "__main__":
        asyncio.run(save_data_to_file())

        
