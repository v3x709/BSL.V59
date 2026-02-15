from titan.data_s.byte_stream import ByteStream
class PiranhaMessage:
    def __init__(self):
        self.stream = ByteStream()
        self.version = 0
    def encode(self): pass
    def decode(self): pass
    def get_message_type(self): return 0
    def get_message_version(self): return self.version
    def is_server_to_client_message(self): return True
