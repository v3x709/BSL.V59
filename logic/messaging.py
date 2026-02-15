import asyncio, hashlib, os, pysodium
from titan.crypto.pepper import PepperKey, PepperEncrypter
from logic.protocol.laser.s.server_hello_message import ServerHelloMessage
from logic.protocol.laser.s.login_ok_message import LoginOkMessage
from logic.protocol.laser.s.own_home_data_message import OwnHomeDataMessage

class Messaging:
    def __init__(self, transport):
        self.transport, self.pepper_state = transport, 2
        self.session_token, self.secret_key, self.s_nonce = os.urandom(24), os.urandom(32), os.urandom(24)

    def next_message(self, data):
        if len(data) < 7: return data
        msg_type, msg_len, msg_ver = int.from_bytes(data[0:2], 'big'), int.from_bytes(data[2:5], 'big'), int.from_bytes(data[5:7], 'big')
        if len(data) < 7 + msg_len: return data
        payload = data[7:7+msg_len]
        self.read_new_message(msg_type, msg_len, msg_ver, payload)
        return data[7+msg_len:]

    def read_new_message(self, t, l, v, p):
        print(f"New message received: {t}")
        if self.pepper_state == 2 and t == 10100:
            self.pepper_state = 3; self.send(ServerHelloMessage(self.session_token))
        elif self.pepper_state == 3 and t == 10101:
            if self.handle_pepper_login(p): self.send(LoginOkMessage()); self.send(OwnHomeDataMessage())
        elif self.pepper_state == 5:
            try: dp = self.decrypt_stream.decrypt(p)
            except: pass

    def handle_pepper_login(self, p):
        try:
            self.client_pk = p[0:32]
            h = hashlib.blake2b(digest_size=24); h.update(self.client_pk); h.update(PepperKey.SERVER_PUBLIC_KEY)
            d = pysodium.crypto_box_open(p[32:], h.digest(), self.client_pk, PepperKey.SERVER_SECRET_KEY)
            if d[0:24] != self.session_token: return False
            self.r_nonce, self.pepper_state = d[24:48], 4
            return True
        except: return False

    def send(self, m):
        if self.pepper_state == 3 and m.get_message_type() == 20100: m.token = self.session_token
        m.encode(); p = m.stream.get_buffer()
        if self.pepper_state == 4: p = self.send_pepper_login_response(p)
        elif self.pepper_state == 5: p = self.encrypt_stream.encrypt(p)
        h = m.get_message_type().to_bytes(2,'big') + len(p).to_bytes(3,'big') + m.get_message_version().to_bytes(2,'big')
        self.transport.write(h + p); print(f"Sent: {m.get_message_type()}")

    def send_pepper_login_response(self, p):
        pkt = self.s_nonce + self.secret_key + p
        h = hashlib.blake2b(digest_size=24); h.update(self.r_nonce); h.update(self.client_pk); h.update(PepperKey.SERVER_PUBLIC_KEY)
        enc = pysodium.crypto_box(bytes(pkt), h.digest(), self.client_pk, PepperKey.SERVER_SECRET_KEY)
        self.decrypt_stream, self.encrypt_stream, self.pepper_state = PepperEncrypter(self.secret_key, self.r_nonce), PepperEncrypter(self.secret_key, self.s_nonce), 5
        return enc
