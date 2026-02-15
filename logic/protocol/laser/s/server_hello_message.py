from logic.protocol.piranha_message import PiranhaMessage

class ServerHelloMessage(PiranhaMessage):
    def __init__(self, session_token):
        super().__init__()
        self.session_token = session_token

    def encode(self):
        self.stream.write_int(len(self.session_token))
        self.stream.buffer.extend(self.session_token)
        self.stream.offset += len(self.session_token)

    def get_message_type(self):
        return 20100
