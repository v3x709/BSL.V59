import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.secret import SecretBox
import hashlib

class PepperKey:
    # ServerSecretKey = Convert.FromHexString("48d7d188d2c4b263233e1f0816bf231e8a3756e280a80083b47d8104e9d002da");
    SERVER_SECRET_KEY = bytes.fromhex("48d7d188d2c4b263233e1f0816bf231e8a3756e280a80083b47d8104e9d002da")
    # In TweetNaCl, CryptoScalarmultBase(ServerSecretKey) gives the public key.
    # In PyNaCl, PrivateKey(seed).public_key gives the public key.
    _private_key = PrivateKey(SERVER_SECRET_KEY)
    SERVER_PUBLIC_KEY = bytes(_private_key.public_key)

class PepperEncrypter:
    def __init__(self, key, nonce):
        self.key = key
        self.nonce = bytearray(nonce)

    def encrypt(self, data):
        if not data:
            return b''
        self.next_nonce()
        # Pepper uses secretbox which is XSalsa20-Poly1305
        box = SecretBox(self.key)
        # nacl.secret.SecretBox.encrypt(plaintext, nonce)
        # Note: SecretBox.encrypt returns (nonce + ciphertext).
        # But we provide the nonce and we want ONLY the ciphertext (with MAC).
        # In TweetNaCl, it's [MAC(16 bytes)][Ciphertext]
        encrypted = box.encrypt(data, bytes(self.nonce))
        return encrypted.ciphertext

    def decrypt(self, data):
        if not data:
            return b''
        self.next_nonce()
        box = SecretBox(self.key)
        # nacl.secret.SecretBox.decrypt(ciphertext, nonce)
        # data here should include the 16-byte MAC.
        return box.decrypt(data, bytes(self.nonce))

    def next_nonce(self):
        v8 = 2
        for i in range(24):
            v10 = v8 + (self.nonce[i] & 0xFF)
            self.nonce[i] = v10 & 0xFF
            v8 = v10 >> 8
            if v8 == 0:
                break

    def get_encryption_overhead(self):
        return 16
