import asyncio
from logic.messaging import Messaging

class LobbyServer:
    async def handle(self, r, w):
        print(f"Connected: {w.get_extra_info('peername')}")
        m, b = Messaging(w), bytearray()
        try:
            while True:
                d = await r.read(4096)
                if not d: break
                b.extend(d)
                while len(b) >= 7:
                    rem = m.next_message(b)
                    if rem == b: break
                    b = bytearray(rem)
        except: pass
        finally: w.close()

    async def start(self):
        s = await asyncio.start_server(self.handle, '0.0.0.0', 9339)
        print("LobbyServer starting (9339)...")
        async with s: await s.serve_forever()

if __name__ == '__main__': asyncio.run(LobbyServer().start())
