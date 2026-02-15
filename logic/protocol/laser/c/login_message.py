from logic.protocol.piranha_message import PiranhaMessage

class LoginMessage(PiranhaMessage):
    def __init__(self, payload):
        super().__init__()
        self.stream.buffer = bytearray(payload)
        self.stream.length = len(payload)

    def decode(self):
        self.account_id_high = self.stream.read_int()
        self.account_id_low = self.stream.read_int()
        self.token = self.stream.read_string()
        self.client_major_version = self.stream.read_int()
        self.client_build_version = self.stream.read_int()
        self.client_content_version = self.stream.read_int()
        self.environment = self.stream.read_string()
        # ... more fields
