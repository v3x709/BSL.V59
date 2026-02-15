from logic.protocol.piranha_message import PiranhaMessage
class LoginOkMessage(PiranhaMessage):
    def encode(self):
        bs = self.stream
        bs.write_int(0); bs.write_int(1) # Account ID
        bs.write_int(0); bs.write_int(1) # Home ID
        bs.write_string("abcdefghijklmnopqrstuvwxyz")
        bs.write_string(""); bs.write_string("")
        bs.write_int(59); bs.write_int(197); bs.write_int(1)
        bs.write_string("dev")
        bs.write_int(0); bs.write_int(0); bs.write_int(0)
        bs.write_string(""); bs.write_string(""); bs.write_string("")
        bs.write_int(0); bs.write_string(""); bs.write_string("RU"); bs.write_string("")
        bs.write_int(0); bs.write_string("")
        bs.write_int(2)
        bs.write_string("https://game-assets.brawlstarsgame.com")
        bs.write_string("http://a678dbc1c015a893c9fd-4e8cc3b1ad3a3c940c504815caefa967.r87.cf2.rackcdn.com")
        bs.write_int(2)
        bs.write_string("https://event-assets.brawlstars.com")
        bs.write_string("https://24b999e6da07674e22b0-8209975788a0f2469e68e84405ae4fcf.ssl.cf2.rackcdn.com/event-assets")
        bs.write_vint(0); bs.write_string("")
        bs.write_boolean(True); bs.write_boolean(False)
        for _ in range(5): bs.write_string("")
        for _ in range(5): bs.write_boolean(False)
    def get_message_type(self): return 20104
