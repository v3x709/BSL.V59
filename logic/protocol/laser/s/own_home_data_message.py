from logic.protocol.piranha_message import PiranhaMessage
from titan.data_s.logic_long import LogicLong
class ByteStreamHelper:
    @staticmethod
    def write_data_reference(stream, csv_id, index=0):
        stream.write_vint(csv_id); stream.write_vint(index)
    @staticmethod
    def encode_logic_long(stream, low, high=0):
        stream.write_vint(high); stream.write_vint(low)
class OwnHomeDataMessage(PiranhaMessage):
    def encode(self):
        bs = self.stream
        bs.write_vint(0); bs.write_vint(-1)
        bs.write_vint(0); bs.write_vint(0)
        bs.write_vint(70000); bs.write_vint(70000); bs.write_vint(70000); bs.write_vint(454); bs.write_vint(1488)
        ByteStreamHelper.write_data_reference(bs, 28, 677); ByteStreamHelper.write_data_reference(bs, 43, 0)
        for _ in range(8): bs.write_vint(0)
        bs.write_vint(70000); bs.write_vint(0); bs.write_vint(1); bs.write_boolean(True)
        bs.write_vint(19500); bs.write_vint(111111); bs.write_vint(1375134); bs.write_vint(0); bs.write_vint(1375134)
        for _ in range(3): bs.write_vint(0)
        bs.write_boolean(True); bs.write_vint(2); bs.write_vint(2); bs.write_vint(2); bs.write_vint(0); bs.write_vint(0)
        bs.write_vint(0) # shop
        bs.write_vint(200); bs.write_vint(-1); bs.write_vint(0); bs.write_vint(0); bs.write_vint(-1)
        bs.write_byte(1); ByteStreamHelper.write_data_reference(bs, 16, 89)
        bs.write_string("RU"); bs.write_string("BSL.v59")
        bs.write_vint(8)
        for h, l in [(1,9),(1,22),(3,25),(1,24),(2,15),(9889434,28),(100,46),(1,52)]: LogicLong(h, l).encode(bs)
        bs.write_vint(0); bs.write_vint(1); bs.write_vint(34); bs.write_vint(0); bs.write_boolean(False); bs.write_vint(0)
        bs.write_boolean(False); bs.write_boolean(True); [bs.write_int(0) for _ in range(4)]
        bs.write_boolean(True); [bs.write_int(0) for _ in range(4)]
        bs.write_boolean(False); bs.write_boolean(True); [bs.write_int(0) for _ in range(4)]
        if bs.write_boolean(True): [bs.write_vint(0) for _ in range(4)]
        if bs.write_boolean(True): bs.write_vint(0)
        bs.write_boolean(False); bs.write_int(0); bs.write_vint(0); ByteStreamHelper.write_data_reference(bs, 16, 0)
        bs.write_boolean(False); bs.write_vint(-1); bs.write_vint(0); bs.write_vint(0); bs.write_vint(0); bs.write_vint(0)
        bs.write_vint(-1); bs.write_vint(38); [bs.write_vint(i+1) for i in range(38)]
        bs.write_vint(1); bs.write_vint(-1); bs.write_vint(1); bs.write_vint(0); bs.write_vint(0); bs.write_vint(85926); bs.write_vint(5); ByteStreamHelper.write_data_reference(bs, 15, 13)
        bs.write_vint(-1); bs.write_vint(0); bs.write_string(None); [bs.write_vint(0) for _ in range(6)]
        bs.write_boolean(False); bs.write_boolean(False); bs.write_vint(0); bs.write_boolean(False); bs.write_vint(0); bs.write_vint(0)
        [bs.write_boolean(False) for _ in range(4)]; bs.write_vint(-1); bs.write_boolean(False); bs.write_boolean(False)
        [bs.write_vint(-1) for _ in range(4)]; [bs.write_boolean(False) for _ in range(4)]; bs.write_vint(0)
        bs.write_vint(10); [bs.write_vint(x) for x in [20, 35, 75, 140, 290, 480, 800, 1250, 1875, 2800]]
        bs.write_vint(4); [bs.write_vint(x) for x in [30, 80, 170, 360]]
        bs.write_vint(4); [bs.write_vint(x) for x in [300, 880, 2040, 4680]]
        bs.write_vint(0)
        res = [(501, 10008), (0, 10046), (30, 10050), (0, 10051), (5600, 10060), (200, 117), (1, 128), (0, 65), (41000000+117, 1), (99999999, 131), (100000, 138), (1, 95), (55598, 47), (1, 123), (200, 124), (55598, 48), (3, 50), (500, 1100), (500, 1101), (1, 1002), (500, 1102)]
        bs.write_vint(len(res)); [LogicLong(h, l).encode(bs) for h, l in res]
        [bs.write_vint(0) for _ in range(8)]
        bs.write_vint(6); [bs.write_vint(x) for x in [0, 29, 79, 169, 349, 699]]
        bs.write_vint(6); [bs.write_vint(x) for x in [0, 160, 450, 500, 1250, 2500]]
        bs.write_vint(5); [bs.write_vint(x) for x in [0, 100, 400, 1000, 3000]]
        LogicLong(0, 1).encode(bs); bs.write_vint(0); bs.write_vint(-1); bs.write_boolean(False); [bs.write_vint(0) for _ in range(3)]
        bs.write_boolean(False); bs.write_boolean(False); bs.write_boolean(False); bs.write_vint(0); bs.write_boolean(True)
        bs.write_vint(0); bs.write_vint(0); bs.write_vint(0); bs.write_vint(1); ByteStreamHelper.write_data_reference(bs, 16, 90)
        [bs.write_vint(x) for x in [1900, 349, 0, 0, 0, 0]]; [bs.write_vint(0) for _ in range(3)]; bs.write_vint(0)
        [ByteStreamHelper.write_data_reference(bs, 0) for _ in range(5)]; [bs.write_boolean(False) for _ in range(4)]
        [bs.write_vint(0) for _ in range(3)]; bs.write_int(-1488); [bs.write_vint(0) for _ in range(2)]; bs.write_vint(51998)
        [bs.write_vint(0) for _ in range(7)]; bs.write_boolean(False); bs.write_boolean(False); bs.write_boolean(False); bs.write_boolean(False)
        bs.write_vint(2); ByteStreamHelper.write_data_reference(bs, 95, 0); bs.write_vint(1); ByteStreamHelper.write_data_reference(bs, 95, 1); bs.write_vint(1); bs.write_boolean(False)
        ByteStreamHelper.encode_logic_long(bs, 1); ByteStreamHelper.encode_logic_long(bs, 1); ByteStreamHelper.encode_logic_long(bs, 0)
        bs.write_string_reference("LkPrtctrd"); bs.write_boolean(True); bs.write_int(-1); bs.write_vint(23)
        for i in range(23):
            if i == 0: bs.write_vint(1); ByteStreamHelper.write_data_reference(bs, 23, 0); bs.write_vint(-1); bs.write_vint(1)
            else: bs.write_vint(0)
        [bs.write_vint(x) for x in [1337, 1337, 0, 100, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0]]; bs.write_string(None); bs.write_vint(0); bs.write_vint(0); bs.write_vint(2)
    def get_message_type(self): return 24101
