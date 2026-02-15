from logic.protocol.piranha_message import PiranhaMessage
from titan.data_s.logic_long import LogicLong

class OwnHomeDataMessage(PiranhaMessage):
    def __init__(self, player_data=None):
        super().__init__()
        if player_data is None:
            self.player_data = {
                'id_high': 0, 'id_low': 1, 'name': 'Player',
                'trophies': 0, 'highest_trophies': 0, 'exp_points': 0,
                'gems': 0, 'gold': 0, 'star_points': 0, 'ranked_points': 0,
                'brawlers': {"0": {"id": 16000000, "skin": 29000000, "trophies": 0, "highest_trophies": 0, "level": 1, "points": 0}}
            }
        elif hasattr(player_data, 'to_dict'):
            self.player_data = player_data.to_dict()
        else:
            self.player_data = player_data

    def encode(self):
        # LogicClientHome start
        self.stream.write_vint(0)
        self.stream.write_vint(-1)

        # LogicDailyData start
        self.stream.write_vint(0)
        self.stream.write_vint(0)

        self.stream.write_vint(self.player_data['trophies'])
        self.stream.write_vint(self.player_data['highest_trophies'])
        self.stream.write_vint(self.player_data['highest_trophies'])
        self.stream.write_vint(self.player_data['exp_points'])

        # Profile icons, etc.
        self.stream.write_vint(1488) # dummy
        self.stream.write_vint(28) # csv
        self.stream.write_vint(677) # index
        self.stream.write_vint(43)
        self.stream.write_vint(0)

        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)

        self.stream.write_vint(70000)
        self.stream.write_vint(0)
        self.stream.write_vint(1)
        self.stream.write_boolean(True)
        self.stream.write_vint(19500)
        self.stream.write_vint(111111)
        self.stream.write_vint(1375134)
        self.stream.write_vint(0)
        self.stream.write_vint(1375134)

        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)

        self.stream.write_boolean(True)
        self.stream.write_vint(2)
        self.stream.write_vint(2)
        self.stream.write_vint(2)
        self.stream.write_vint(0)
        self.stream.write_vint(0)

        # Shop offers
        self.stream.write_vint(1) # One welcome reward
        self.stream.write_vint(1) # Offer index
        self.stream.write_vint(1) # Offer type
        self.stream.write_vint(1) # Items count
        self.stream.write_vint(100) # Amount
        self.stream.write_vint(0) # Item ID
        self.stream.write_vint(1) # Item Type
        self.stream.write_vint(0)
        self.stream.write_vint(0) # Price
        self.stream.write_vint(0) # Price Type
        self.stream.write_vint(1) # Availability
        self.stream.write_vint(86400) # Time left
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_boolean(False)

        self.stream.write_vint(200)
        self.stream.write_vint(-1)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(-1)

        self.stream.write_byte(1)
        self.stream.write_vint(16)
        self.stream.write_vint(89)

        self.stream.write_string("RU")
        self.stream.write_string("BSL.v59-Python")

        self.stream.write_vint(0) # LogicLong Array
        self.stream.write_vint(0)
        self.stream.write_vint(0)

        self.stream.write_boolean(False)
        self.stream.write_boolean(False)
        self.stream.write_boolean(False)
        # ... many more fields from C# ...

        # LogicDailyData end
        # LogicConfData start (Simplified)
        self.stream.write_vint(-1)
        self.stream.write_vint(0) # array
        self.stream.write_vint(0) # array
        self.stream.write_vint(0) # array
        self.stream.write_vint(0) # array
        self.stream.write_vint(0) # array
        # LogicConfData end

        # Avatar logic
        self.stream.write_vint(self.player_data['id_high'])
        self.stream.write_vint(self.player_data['id_low'])
        self.stream.write_vint(self.player_data['id_high'])
        self.stream.write_vint(self.player_data['id_low'])
        self.stream.write_vint(0)

        self.stream.write_string(self.player_data['name'])
        self.stream.write_boolean(True)
        self.stream.write_int(-1)

        # Brawlers (CSV 23)
        brawlers = self.player_data['brawlers']
        self.stream.write_vint(len(brawlers))
        for b_idx, stats in brawlers.items():
            self.stream.write_vint(23) # character csv
            self.stream.write_vint(int(b_idx)) # Shelly is 0
            self.stream.write_vint(-1)
            self.stream.write_vint(stats['level'])

        # Currencies and other stats
        self.stream.write_vint(self.player_data['gems'])
        self.stream.write_vint(self.player_data['exp_points'])
        self.stream.write_vint(100) # Profile icon
        self.stream.write_vint(0) # Name color
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(2)
        self.stream.write_vint(1)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_string(None)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(2)

    def get_message_type(self):
        return 24101
