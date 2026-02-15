from protocol.piranha_message import PiranhaMessage

class ClientHelloMessage(PiranhaMessage):
    def __init__(self, payload=None):
        super().__init__()
        if payload:
            self.stream.buffer = bytearray(payload)
            self.stream.length = len(payload)

    def decode(self):
        self.protocol = self.stream.read_int()
        self.key_version = self.stream.read_int()
        self.major_version = self.stream.read_int()
        self.build_version = self.stream.read_int()
        self.content_version = self.stream.read_int()
        self.fingerprint_sha = self.stream.read_string()

    def get_message_type(self):
        return 10100

class LoginMessage(PiranhaMessage):
    def __init__(self, payload=None):
        super().__init__()
        if payload:
            self.stream.buffer = bytearray(payload)
            self.stream.length = len(payload)

    def decode(self):
        self.account_id_high = self.stream.read_int()
        self.account_id_low = self.stream.read_int()
        self.token = self.stream.read_string()
        self.major_version = self.stream.read_int()
        self.build_version = self.stream.read_int()
        self.content_version = self.stream.read_int()
        self.environment = self.stream.read_string()
        # ... more fields are usually there in v59

    def get_message_type(self):
        return 10101
