from logic.protocol.piranha_message import PiranhaMessage
class BattleEndMessage(PiranhaMessage):
    def __init__(self, rgain, tgain):
        super().__init__()
        self.rgain, self.tgain = rgain, tgain
    def encode(self):
        bs = self.stream
        bs.write_vint(1) # Type
        bs.write_vint(self.tgain)
        bs.write_vint(self.rgain)
        bs.write_vint(1) # Result
        bs.write_vint(0); bs.write_vint(0); bs.write_vint(0)
        bs.write_vint(1) # Players
        bs.write_vint(16000000); bs.write_vint(0); bs.write_string("Player")
    def get_message_type(self): return 25281
