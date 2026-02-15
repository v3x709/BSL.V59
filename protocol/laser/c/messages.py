from protocol.piranha_message import PiranhaMessage

class LoginMessage(PiranhaMessage):
    def __init__(self, payload=None):
        super().__init__()
        if payload:
            self.stream.buffer = bytearray(payload)
            self.stream.offset = 0
            self.stream.bit_idx = 0

    def decode(self):
        self.account_id_high = self.stream.read_int()
        self.account_id_low = self.stream.read_int()
        self.pass_token = self.stream.read_string()
        self.client_major_version = self.stream.read_int()
        self.client_minor = self.stream.read_int()
        self.client_build = self.stream.read_int()
        self.resource_sha = self.stream.read_string()

    def get_message_type(self):
        return 10101
