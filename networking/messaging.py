import asyncio, hashlib, os, pysodium
from crypto.pepper import PepperKey, PepperEncrypter
from protocol.laser.s.messages import ServerHelloMessage, LoginOkMessage, OwnHomeDataMessage, BattleEndMessage, MatchmakingStatusMessage, StartLoadingMessage
from protocol.laser.c.messages import ClientHelloMessage, LoginMessage
from logic.message_manager import MessageManager

class Messaging:
    def __init__(self, transport, db_manager):
        self.transport, self.db_manager, self.pepper_state = transport, db_manager, 2
        self.session_token, self.secret_key, self.s_nonce = os.urandom(24), os.urandom(32), os.urandom(24)
        self.message_manager = MessageManager(self)
        self.player_data = None
        self.client_pk = None
        self.r_nonce = None
        self.decrypt_stream = None
        self.encrypt_stream = None

    def next_message(self, data):
        if len(data) < 7: return data
        t = int.from_bytes(data[0:2], 'big')
        l = int.from_bytes(data[2:5], 'big')
        v = int.from_bytes(data[5:7], 'big')
        if len(data) < 7 + l: return data
        p = data[7:7+l]
        self.read_new_message(t, l, v, p)
        return data[7+l:]

    def read_new_message(self, t, l, v, p):
        print(f"New message received: {t}")
        if self.pepper_state == 2 and t == 10100:
            self.pepper_state = 3; self.send(ServerHelloMessage(self.session_token))
        elif self.pepper_state == 3 and t == 10101:
            decrypted = self.handle_pepper_login(p)
            if decrypted:
                login_msg = LoginMessage(decrypted)
                self.message_manager.receive_message(login_msg)
        elif self.pepper_state == 5:
            try:
                dp = self.decrypt_stream.decrypt(p)
                if t == 10108: self.handle_matchmaking()
            except Exception as e:
                print(f"Decryption error: {e}")

    def handle_matchmaking(self):
        asyncio.create_task(self.run_battle())

    async def run_battle(self):
        self.send(MatchmakingStatusMessage())
        await asyncio.sleep(1)
        self.send(StartLoadingMessage())

        from logic.battle import BattleSimulation
        sim = BattleSimulation(self.player_data['id_low'] if self.player_data else 0)
        await sim.run(self)

        from logic.player import Player
        player = Player(self.player_data)
        rg, tg = player.process_win()
        self.db_manager.update_player(player.to_dict())

        self.send(BattleEndMessage(rg, tg))

    def handle_pepper_login(self, p):
        try:
            self.client_pk = p[0:32]
            h = hashlib.blake2b(digest_size=24); h.update(self.client_pk); h.update(PepperKey.SERVER_PUBLIC_KEY)
            d = pysodium.crypto_box_open(p[32:], h.digest(), self.client_pk, PepperKey.SERVER_SECRET_KEY)
            if d[0:24] != self.session_token: return None
            self.r_nonce, self.pepper_state = d[24:48], 4
            return d[48:]
        except: return None

    def send(self, m):
        if self.pepper_state == 3 and m.get_message_type() == 20100: m.session_token = self.session_token
        m.encode(); p = m.stream.get_buffer()
        if self.pepper_state == 4: p = self.send_pepper_login_response(p)
        elif self.pepper_state == 5: p = self.encrypt_stream.encrypt(p)
        h = m.get_message_type().to_bytes(2,'big') + len(p).to_bytes(3,'big') + m.get_message_version().to_bytes(2,'big')
        self.transport.write(h + p); print(f"Sent: {m.get_message_type()}")

    def send_pepper_login_response(self, p):
        pkt = self.s_nonce + self.secret_key + p
        h = hashlib.blake2b(digest_size=24); h.update(self.r_nonce); h.update(self.client_pk); h.update(PepperKey.SERVER_PUBLIC_KEY)
        enc = pysodium.crypto_box(bytes(pkt), h.digest(), self.client_pk, PepperKey.SERVER_SECRET_KEY)
        self.decrypt_stream = PepperEncrypter(self.secret_key, self.r_nonce)
        self.encrypt_stream = PepperEncrypter(self.secret_key, self.s_nonce)
        self.pepper_state = 5
        return enc
