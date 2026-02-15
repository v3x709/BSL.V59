class LogicLong:
    def __init__(self, high=0, low=0):
        self.high = high
        self.low = low
    def encode(self, stream):
        stream.write_vint(self.high)
        stream.write_vint(self.low)
