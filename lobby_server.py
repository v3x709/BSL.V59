import asyncio
from logic.messaging import Messaging
from database.db_manager import DatabaseManager
import sys
import os


class LobbyServer:
    def __init__(self, host='0.0.0.0', port=9339):
        self.host = host
        self.port = port
        self.db_manager = DatabaseManager()

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"New user connected! RAddress: {addr}")

        messaging = Messaging(writer, self.db_manager)
        buffer = bytearray()

        try:
            while True:
                data = await reader.read(4096)
                if not data:
                    break

                buffer.extend(data)
                while len(buffer) >= 7:
                    # process_buffer returns remaining data
                    remaining = messaging.next_message(buffer)
                    if remaining == buffer: # Not enough data for a full message
                        break
                    buffer = bytearray(remaining)
        except ConnectionResetError:
            print(f"Connection reset by {addr}")
        except Exception as e:
            print(f"Exception in handle_client: {e}")
        finally:
            print(f"User disconnected! RAddress: {addr}")
            writer.close()
            await writer.wait_closed()

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f'LobbyServer starting ({self.port}) ...')
        async with server:
            await server.serve_forever()

if __name__ == '__main__':
    server = LobbyServer()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        pass
