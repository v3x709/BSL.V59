from logic.protocol.piranha_message import PiranhaMessage

class MatchmakingStatusMessage(PiranhaMessage):
    def __init__(self):
        super().__init__()

    def encode(self):
        self.stream.write_int(0) # Time passed
        self.stream.write_int(6) # Players found
        self.stream.write_int(6) # Max players
        self.stream.write_int(0)
        self.stream.write_boolean(False)

    def get_message_type(self):
        return 20405

class StartLoadingMessage(PiranhaMessage):
    def __init__(self):
        super().__init__()

    def encode(self):
        self.stream.write_int(6) # Players count
        for i in range(6):
            self.stream.write_int(0) # High
            self.stream.write_int(i + 1) # Low
            self.stream.write_vint(0)
            self.stream.write_vint(0)
            self.stream.write_vint(16) # Character ID (Shelly)
            self.stream.write_vint(29) # Skin ID
            self.stream.write_vint(0)
            self.stream.write_vint(0)
            self.stream.write_vint(0)
            self.stream.write_string(f"Bot {i+1}" if i > 0 else "Player")
            self.stream.write_vint(0)
            self.stream.write_vint(0)
            self.stream.write_vint(10) # Level
            self.stream.write_vint(1)
            self.stream.write_vint(1)
            self.stream.write_vint(1)
            self.stream.write_vint(1)

        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)

        self.stream.write_int(1) # Map index
        self.stream.write_vint(0)
        self.stream.write_vint(0)

    def get_message_type(self):
        return 20410
