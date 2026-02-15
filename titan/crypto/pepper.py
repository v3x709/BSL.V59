import pysodium
import hashlib

class PepperKey:
    # ServerSecretKey = Convert.FromHexString("48d7d188d2c4b263233e1f0816bf231e8a3756e280a80083b47d8104e9d002da");
    SERVER_SECRET_KEY = bytes.fromhex("48d7d188d2c4b263233e1f0816bf231e8a3756e280a80083b47d8104e9d002da")
    # In TweetNaCl/libsodium, crypto_scalarmult_base gives the public key from secret key.
    SERVER_PUBLIC_KEY = pysodium.crypto_scalarmult_base(SERVER_SECRET_KEY)

class PepperEncrypter:
    def __init__(self, key, nonce):
        self.key = key
        self.nonce = bytearray(nonce)

    def encrypt(self, data):
        if not data:
            return b''
        self.next_nonce()
        # Pepper uses secretbox which is XSalsa20-Poly1305
        # pysodium.crypto_secretbox(message, nonce, key)
        # Returns the ciphertext with the MAC prepended (16 bytes).
        return pysodium.crypto_secretbox(data, bytes(self.nonce), self.key)

    def decrypt(self, data):
        if not data:
            return b''
        self.next_nonce()
        # pysodium.crypto_secretbox_open(ciphertext, nonce, key)
        return pysodium.crypto_secretbox_open(data, bytes(self.nonce), self.key)

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
