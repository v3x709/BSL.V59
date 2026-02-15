from logic.protocol.piranha_message import PiranhaMessage
class ServerHelloMessage(PiranhaMessage):
    def __init__(self, token=None):
        super().__init__()
        self.token = token
    def encode(self): self.stream.write_bytes(self.token)
    def get_message_type(self): return 20100
