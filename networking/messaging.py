import asyncio, hashlib, os, pysodium
from crypto.pepper import PepperKey, PepperEncrypter
from protocol.laser.s.messages import ServerHelloMessage, LoginOkMessage, OwnHomeDataMessage
from protocol.laser.c.messages import ClientHelloMessage, LoginMessage
from database.db_manager import DatabaseManager
from logic.player import Player

class Messaging:
    def __init__(self, transport, db_manager):
        self.transport, self.db_manager, self.pepper_state = transport, db_manager, 2
        self.session_token, self.secret_key, self.s_nonce = os.urandom(24), os.urandom(32), os.urandom(24)
        self.player = None

    def next_message(self, data):
        if len(data) < 7: return data
        msg_type = int.from_bytes(data[0:2], 'big')
        msg_len = int.from_bytes(data[2:5], 'big')
        msg_ver = int.from_bytes(data[5:7], 'big')
        if len(data) < 7 + msg_len: return data
        payload = data[7:7+msg_len]
        self.read_new_message(msg_type, msg_len, msg_ver, payload)
        return data[7+msg_len:]

    def read_new_message(self, t, l, v, p):
        print(f"New message received: {t}")
        if self.pepper_state == 2 and t == 10100:
            self.pepper_state = 3; self.send(ServerHelloMessage(self.session_token))
        elif self.pepper_state == 3 and t == 10101:
            decrypted = self.handle_pepper_login(p)
            if decrypted:
                login_msg = LoginMessage(decrypted); login_msg.decode()
                id_low = login_msg.account_id_low
                if id_low == 0:
                    id_low = self.db_manager.get_max_id_low() + 1
                    import secrets
                    token = secrets.token_hex(16)
                    self.db_manager.create_player(0, id_low, token)

                player_data = self.db_manager.get_player(0, id_low)
                if not player_data:
                    self.db_manager.create_player(0, id_low, "token")
                    player_data = self.db_manager.get_player(0, id_low)

                self.player_data = player_data
                self.send(LoginOkMessage()); self.send(OwnHomeDataMessage(self.player_data))
        elif self.pepper_state == 5:
            try:
                dp = self.decrypt_stream.decrypt(p)
                # Handle complex logic here
            except: pass

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
