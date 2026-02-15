from logic.protocol.piranha_message import PiranhaMessage
import random

class BattleEndMessage(PiranhaMessage):
    def __init__(self, trophy_gain, ranked_gain):
        super().__init__()
        self.trophy_gain = trophy_gain
        self.ranked_gain = ranked_gain

    def encode(self):
        self.stream.write_vint(1) # Battle type?
        self.stream.write_vint(self.trophy_gain)
        self.stream.write_vint(self.ranked_gain)

        self.stream.write_vint(1) # Result (Win)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)

        # Brawlers stats update
        self.stream.write_vint(1) # Players count
        self.stream.write_vint(16000000) # Shelly
        self.stream.write_vint(0)
        self.stream.write_string("Player")

    def get_message_type(self):
        return 25281 # Common ID for BattleEnd

class VisionUpdateMessage(PiranhaMessage):
    # This is for real-time UDP vision, but can be sent over TCP in some cases
    def get_message_type(self):
        return 24109
