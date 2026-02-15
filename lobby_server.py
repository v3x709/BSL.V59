import asyncio
from networking.messaging import Messaging
from database.db_manager import DatabaseManager

class LobbyServer:
    def __init__(self, host='0.0.0.0', port=9339):
        self.host, self.port = host, port
        self.db_manager = DatabaseManager()

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connected: {addr}")
        m, b = Messaging(writer, self.db_manager), bytearray()
        try:
            while True:
                d = await reader.read(4096)
                if not d: break
                b.extend(d)
                while len(b) >= 7:
                    rem = m.next_message(b)
                    if rem == b: break
                    b = bytearray(rem)
        except: pass
        finally: writer.close()

    async def start(self):
        s = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"LobbyServer starting ({self.port})...")
        async with s: await s.serve_forever()

if __name__ == '__main__':
    asyncio.run(LobbyServer().start())
