from logic.protocol.piranha_message import PiranhaMessage
from titan.data_s.logic_long import LogicLong

class ByteStreamHelper:
    @staticmethod
    def write_data_reference(stream, csv_id, index=0):
        stream.write_vint(csv_id)
        stream.write_vint(index)

    @staticmethod
    def encode_logic_long(stream, low, high=0):
        stream.write_vint(high)
        stream.write_vint(low)

class OwnHomeDataMessage(PiranhaMessage):
    def __init__(self, player=None):
        super().__init__()
        self.player = player

    def encode(self):
        # LogicClientHome start
        self.stream.write_vint(0)
        self.stream.write_vint(-1)

        # LogicDailyData start
        self.stream.write_vint(0)
        self.stream.write_vint(0)

        trophies = self.player.trophies if self.player else 0
        highest_trophies = self.player.highest_trophies if self.player else 0
        exp_points = self.player.exp_points if self.player else 0
        gems = self.player.gems if self.player else 0
        gold = self.player.gold if self.player else 0
        star_points = self.player.star_points if self.player else 0
        ranked_points = self.player.ranked_points if self.player else 0

        self.stream.write_vint(trophies)
        self.stream.write_vint(highest_trophies)
        self.stream.write_vint(highest_trophies)
        self.stream.write_vint(exp_points)
        self.stream.write_vint(1488) # dummy
        ByteStreamHelper.write_data_reference(self.stream, 28, 677)
        ByteStreamHelper.write_data_reference(self.stream, 43, 0)

        for _ in range(8):
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

        self.stream.write_vint(1) # One welcome reward
        self.stream.write_vint(1) # Offer index
        self.stream.write_vint(1) # Offer type
        self.stream.write_vint(1) # Items count
        self.stream.write_vint(100) # Amount (100 gems)
        self.stream.write_vint(0) # Item ID
        self.stream.write_vint(1) # Item Type (Gems)
        self.stream.write_vint(0)
        self.stream.write_vint(0) # Price
        self.stream.write_vint(0) # Price Type
        self.stream.write_vint(1) # Availability
        self.stream.write_vint(86400) # Time left
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_boolean(False) # Bought

        self.stream.write_vint(200)
        self.stream.write_vint(-1)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(-1)

        self.stream.write_byte(1)
        ByteStreamHelper.write_data_reference(self.stream, 16, 89)

        self.stream.write_string("RU")
        self.stream.write_string("BSL.v59")

        self.stream.write_vint(8)
        LogicLong(1, 9).encode(self.stream)
        LogicLong(1, 22).encode(self.stream)
        LogicLong(3, 25).encode(self.stream)
        LogicLong(1, 24).encode(self.stream)
        LogicLong(2, 15).encode(self.stream)
        LogicLong(9889434, 28).encode(self.stream)
        LogicLong(100, 46).encode(self.stream)
        LogicLong(1, 52).encode(self.stream)

        self.stream.write_vint(0)

        self.stream.write_vint(1)
        self.stream.write_vint(34)
        self.stream.write_vint(0)
        self.stream.write_boolean(False)
        self.stream.write_vint(0)
        self.stream.write_boolean(False)
        self.stream.write_boolean(True)
        for _ in range(4): self.stream.write_int(0)
        self.stream.write_boolean(True)
        for _ in range(4): self.stream.write_int(0)
        self.stream.write_boolean(False)
        self.stream.write_boolean(True)
        for _ in range(4): self.stream.write_int(0)

        if self.stream.write_boolean(True):
            for _ in range(4): self.stream.write_vint(0)

        if self.stream.write_boolean(True):
            self.stream.write_vint(0)

        self.stream.write_boolean(False)
        self.stream.write_int(0)
        self.stream.write_vint(0)
        ByteStreamHelper.write_data_reference(self.stream, 16, 0)
        self.stream.write_boolean(False)
        self.stream.write_vint(-1)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        # LogicDailyData end

        # LogicConfData start
        self.stream.write_vint(-1)
        self.stream.write_vint(38)
        for i in range(38):
            self.stream.write_vint(i + 1)

        self.stream.write_vint(1)
        self.stream.write_vint(-1)
        self.stream.write_vint(1)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        self.stream.write_vint(85926)
        self.stream.write_vint(5)
        ByteStreamHelper.write_data_reference(self.stream, 15, 13)
        self.stream.write_vint(-1)
        self.stream.write_vint(0)
        self.stream.write_string(None)
        for _ in range(6): self.stream.write_vint(0)
        self.stream.write_boolean(False)
        self.stream.write_boolean(False)
        self.stream.write_vint(0)
        self.stream.write_boolean(False)
        self.stream.write_vint(0)
        self.stream.write_vint(0)
        for _ in range(4): self.stream.write_boolean(False)
        self.stream.write_vint(-1)
        self.stream.write_boolean(False)
        self.stream.write_boolean(False)
        for _ in range(4): self.stream.write_vint(-1)
        for _ in range(4): self.stream.write_boolean(False)

        self.stream.write_vint(0)
        self.stream.write_vint(10)
        for i in [20, 35, 75, 140, 290, 480, 800, 1250, 1875, 2800]:
            self.stream.write_vint(i)

        self.stream.write_vint(4)
        for i in [30, 80, 170, 360]:
            self.stream.write_vint(i)

        self.stream.write_vint(4)
        for i in [300, 880, 2040, 4680]:
            self.stream.write_vint(i)

        self.stream.write_vint(0)

        # Resources/Points
        resources = [
            (501, 10008), (ranked_points, 10046), (30, 10050), (0, 10051),
            (5600, 10060), (gold, 117), (1, 128), (0, 65),
            (41000000 + 117, 1), (99999999, 131), (100000, 138), (1, 95),
            (55598, 47), (1, 123), (200, 124), (55598, 48), (3, 50),
            (500, 1100), (500, 1101), (1, 1002), (500, 1102)
        ]
        self.stream.write_vint(len(resources))
        for val, kind in resources:
            LogicLong(val, kind).encode(self.stream)

        for _ in range(8):
            self.stream.write_vint(0)

        self.stream.write_vint(6)
        for i in [0, 29, 79, 169, 349, 699]:
            self.stream.write_vint(i)

        self.stream.write_vint(6)
        for i in [0, 160, 450, 500, 1250, 2500]:
            self.stream.write_vint(i)

        self.stream.write_vint(5)
        for i in [0, 100, 400, 1000, 3000]:
            self.stream.write_vint(i)
        # LogicConfData end

        LogicLong(0, 1).encode(self.stream)
        self.stream.write_vint(0)
        self.stream.write_vint(-1)
        self.stream.write_boolean(False)
        for _ in range(3): self.stream.write_vint(0)
        for _ in range(3): self.stream.write_boolean(False)
        self.stream.write_vint(0)

        self.stream.write_boolean(True)
        for _ in range(3): self.stream.write_vint(0)
        self.stream.write_vint(1)
        ByteStreamHelper.write_data_reference(self.stream, 16, 90)
        for i in [1900, 349, 0, 0, 0, 0]:
            self.stream.write_vint(i)
        for _ in range(4): self.stream.write_vint(0)

        for _ in range(5): ByteStreamHelper.write_data_reference(self.stream, 0, 0)
        for _ in range(4): self.stream.write_boolean(False)

        for _ in range(3): self.stream.write_vint(0)
        self.stream.write_int(-1488)
        for _ in range(2): self.stream.write_vint(0)
        self.stream.write_vint(51998)
        for _ in range(6): self.stream.write_vint(0)
        self.stream.write_boolean(False)

        for _ in range(3): self.stream.write_boolean(False)
        self.stream.write_vint(2)
        ByteStreamHelper.write_data_reference(self.stream, 95, 0)
        self.stream.write_vint(1)
        ByteStreamHelper.write_data_reference(self.stream, 95, 1)
        self.stream.write_vint(1)
        self.stream.write_boolean(False)
        # LogicClientHome end

        # LogicClientAvatar start
        ByteStreamHelper.encode_logic_long(self.stream, 1)
        ByteStreamHelper.encode_logic_long(self.stream, 1)
        ByteStreamHelper.encode_logic_long(self.stream, 0)

        self.stream.write_string_reference("LkPrtctrd")
        self.stream.write_boolean(True)
        self.stream.write_int(-1)

        # Brawlers
        self.stream.write_vint(23)
        for i in range(23):
            if i == 0:
                self.stream.write_vint(1)
                ByteStreamHelper.write_data_reference(self.stream, 23, 0)
                self.stream.write_vint(-1)
                self.stream.write_vint(1)
            else:
                self.stream.write_vint(0)

        self.stream.write_vint(gems)
        self.stream.write_vint(gems)
        self.stream.write_vint(0)
        self.stream.write_vint(100)
        for _ in range(7): self.stream.write_vint(0)
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
