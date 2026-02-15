class LogicLong:
    def __init__(self, high=0, low=0):
        self.high = high
        self.low = low

    def encode(self, stream):
        stream.write_vint(self.high)
        stream.write_vint(self.low)

    def decode(self, stream):
        self.high = stream.read_vint()
        self.low = stream.read_vint()

    @staticmethod
    def read(stream):
        high = stream.read_vint()
        low = stream.read_vint()
        return LogicLong(high, low)
