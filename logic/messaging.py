import asyncio
import hashlib
import os
from titan.data_s.byte_stream import ByteStream
from titan.crypto.pepper import PepperKey, PepperEncrypter
import pysodium
from logic.protocol.laser.s.server_hello_message import ServerHelloMessage
from logic.protocol.laser.s.login_ok_message import LoginOkMessage
from logic.protocol.laser.s.own_home_data_message import OwnHomeDataMessage

class Messaging:
    def __init__(self, transport, db_manager):
        self.transport = transport
        self.db_manager = db_manager
        self.session_token = os.urandom(24)
        self.secret_key = os.urandom(32)
        self.s_nonce = os.urandom(24)
        self.pepper_state = 2
        self.client_pk = None
        self.r_nonce = None
        self.decrypt_stream = None
        self.encrypt_stream = None
        self.player = None

    def next_message(self, data):
        if len(data) < 7:
            return data

        msg_type = int.from_bytes(data[0:2], 'big')
        msg_len = int.from_bytes(data[2:5], 'big')
        msg_ver = int.from_bytes(data[5:7], 'big')

        if len(data) < 7 + msg_len:
            return data

        payload = data[7 : 7 + msg_len]
        self.read_new_message(msg_type, msg_len, msg_ver, payload)

        return data[7 + msg_len:]

    def read_new_message(self, msg_type, msg_len, msg_ver, payload):
        print(f"Received message type: {msg_type}")

        if self.pepper_state == 2:
            if msg_type == 10100:
                self.pepper_state = 3
                self.send(ServerHelloMessage(self.session_token))
            else:
                print("Error: Expected ClientHello (10100)")
                return
        elif self.pepper_state == 3:
            if msg_type == 10101:
                decrypted_payload = self.handle_pepper_login(payload)
                if decrypted_payload:
                    from logic.protocol.laser.c.login_message import LoginMessage
                    login_msg = LoginMessage(decrypted_payload)
                    login_msg.decode()

                    id_high = login_msg.account_id_high
                    id_low = login_msg.account_id_low
                    token = login_msg.token

                    if id_low == 0: # New account
                        id_low = self.db_manager.get_max_id_low() + 1
                        import secrets
                        token = secrets.token_hex(16)
                        self.db_manager.create_player(0, id_low, token)

                    player_data = self.db_manager.get_player(0, id_low)
                    if not player_data:
                        self.db_manager.create_player(0, id_low, token)
                        player_data = self.db_manager.get_player(0, id_low)

                    from logic.player import Player
                    self.player = Player(player_data)

                    self.send(LoginOkMessage())
                    self.send(OwnHomeDataMessage(self.player))
                else:
                    print("Error: Pepper login decryption failed")
                    return
            else:
                print("Error: Expected Login (10101)")
                return
        elif self.pepper_state == 5:
            try:
                decrypted_payload = self.decrypt_stream.decrypt(payload)
                if msg_type == 10108: # MatchmakeRequest
                    print("Matchmaking requested!")
                    self.handle_matchmaking()
                elif msg_type == 14102: # EndClientTurn
                    pass
            except Exception as e:
                print(f"Decryption error: {e}")

    def handle_matchmaking(self):
        asyncio.create_task(self.simulate_battle())

    async def simulate_battle(self):
        from logic.protocol.laser.s.battle_messages import MatchmakingStatusMessage, StartLoadingMessage

        self.send(MatchmakingStatusMessage())
        await asyncio.sleep(1)
        self.send(StartLoadingMessage())

        # 5 seconds of "battle"
        await asyncio.sleep(5)

        if self.player:
            trophy_gain, ranked_gain = self.player.add_battle_reward(win=True)
            self.db_manager.update_player(self.player.to_dict())

            from logic.protocol.laser.s.battle_end_message import BattleEndMessage
            self.send(BattleEndMessage(trophy_gain, ranked_gain))

    def handle_pepper_login(self, payload):
        try:
            self.client_pk = payload[0:32]

            hasher = hashlib.blake2b(digest_size=24)
            hasher.update(self.client_pk)
            hasher.update(PepperKey.SERVER_PUBLIC_KEY)
            nonce = hasher.digest()

            # pysodium.crypto_box_open(ciphertext, nonce, pk, sk)
            # The payload[32:] contains the MAC (16 bytes) + encrypted content.
            # pysodium/libsodium expects the same format.
            decrypted = pysodium.crypto_box_open(payload[32:], nonce, self.client_pk, PepperKey.SERVER_SECRET_KEY)

            if decrypted[0:24] != self.session_token:
                print("Session token mismatch")
                return None

            self.r_nonce = decrypted[24:48]
            self.pepper_state = 4

            return decrypted[48:]
        except Exception as e:
            print(f"Exception in handle_pepper_login: {e}")
            return None

    def send(self, message):
        message.encode()
        payload = message.stream.get_buffer()

        if self.pepper_state == 4:
            payload = self.send_pepper_login_response(payload)
        elif self.pepper_state == 5:
            payload = self.encrypt_stream.encrypt(payload)

        header = self.write_header(payload, message.get_message_type(), message.get_message_version())
        self.transport.write(header + payload)

    def send_pepper_login_response(self, payload):
        packet = bytearray()
        packet.extend(self.s_nonce)
        packet.extend(self.secret_key)
        packet.extend(payload)

        hasher = hashlib.blake2b(digest_size=24)
        hasher.update(self.r_nonce)
        hasher.update(self.client_pk)
        hasher.update(PepperKey.SERVER_PUBLIC_KEY)
        nonce = hasher.digest()

        # pysodium.crypto_box(message, nonce, pk, sk)
        # Returns ciphertext with MAC prepended.
        encrypted = pysodium.crypto_box(bytes(packet), nonce, self.client_pk, PepperKey.SERVER_SECRET_KEY)

        self.decrypt_stream = PepperEncrypter(self.secret_key, self.r_nonce)
        self.encrypt_stream = PepperEncrypter(self.secret_key, self.s_nonce)
        self.pepper_state = 5

        return encrypted

    def write_header(self, payload, msg_type, msg_ver):
        header = bytearray()
        header.extend(msg_type.to_bytes(2, 'big'))
        header.extend(len(payload).to_bytes(3, 'big'))
        header.extend(msg_ver.to_bytes(2, 'big'))
        return header
