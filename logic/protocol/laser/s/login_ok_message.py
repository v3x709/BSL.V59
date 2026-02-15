from logic.protocol.piranha_message import PiranhaMessage

class LoginOkMessage(PiranhaMessage):
    def __init__(self):
        super().__init__()

    def encode(self):
        # Account ID
        self.stream.write_int(0)
        self.stream.write_int(1)

        # Home ID
        self.stream.write_int(0)
        self.stream.write_int(1)

        self.stream.write_string("abcdefghijklmnopqrstuvwxyz") # Token
        self.stream.write_string("") # Facebook ID
        self.stream.write_string("") # Gamecenter ID
        self.stream.write_int(59)
        self.stream.write_int(197)
        self.stream.write_int(1)
        self.stream.write_string("dev")
        self.stream.write_int(0)
        self.stream.write_int(0)
        self.stream.write_int(0)
        self.stream.write_string("")
        self.stream.write_string("")
        self.stream.write_string("")
        self.stream.write_int(0)
        self.stream.write_string("")
        self.stream.write_string("RU")
        self.stream.write_string("")
        self.stream.write_int(0)
        self.stream.write_string("")
        self.stream.write_int(2)
        self.stream.write_string("https://game-assets.brawlstarsgame.com")
        self.stream.write_string("http://a678dbc1c015a893c9fd-4e8cc3b1ad3a3c940c504815caefa967.r87.cf2.rackcdn.com")
        self.stream.write_int(2)
        self.stream.write_string("https://event-assets.brawlstars.com")
        self.stream.write_string("https://24b999e6da07674e22b0-8209975788a0f2469e68e84405ae4fcf.ssl.cf2.rackcdn.com/event-assets")
        self.stream.write_vint(0)
        self.stream.write_string("")
        self.stream.write_boolean(True)
        self.stream.write_boolean(False)
        for _ in range(5): self.stream.write_string("")
        for _ in range(5): self.stream.write_boolean(False)

    def get_message_type(self):
        return 20104
