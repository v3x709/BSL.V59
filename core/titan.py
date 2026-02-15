import struct

class ChecksumEncoder:
    def __init__(self):
        self._checksum = 0
        self._enabled = True
        self._snapshot_checksum = 0

    def enable_checksum(self, enable):
        if not self._enabled or enable:
            if not self._enabled and enable:
                self._checksum = self._snapshot_checksum
            self._enabled = enable
        else:
            self._snapshot_checksum = self._checksum
            self._enabled = False

    def rotate_left(self, val, count):
        return ((val << count) | (val >> (32 - count))) & 0xFFFFFFFF

    def write_short(self, value):
        self._checksum = (value + self.rotate_left(self._checksum, 1) + 19) & 0xFFFFFFFF

    def write_int(self, value):
        self._checksum = (value + self.rotate_left(self._checksum, 1) + 9) & 0xFFFFFFFF

    def write_vint(self, value):
        self._checksum = (value + self.rotate_left(self._checksum, 1) + 33) & 0xFFFFFFFF
        return value

    def write_long_long(self, value):
        self._checksum = (value + self.rotate_left(self._checksum, 1) + 67) & 0xFFFFFFFF

    def write_byte(self, value):
        self._checksum = (value + self.rotate_left(self._checksum, 1) + 11) & 0xFFFFFFFF
        return value

    def write_bytes(self, value, length):
        val = length + 28 if value is not None else 27
        self._checksum = (val + self.rotate_left(self._checksum, 1)) & 0xFFFFFFFF

    def write_boolean(self, value):
        val = 13 if value else 7
        self._checksum = (val + self.rotate_left(self._checksum, 1)) & 0xFFFFFFFF
        return value

    def write_string(self, value):
        val = len(value) + 28 if value is not None else 27
        self._checksum = (val + self.rotate_left(self._checksum, 1)) & 0xFFFFFFFF

    def write_string_reference(self, value):
        val = len(value) if value is not None else 0
        self._checksum = (val + self.rotate_left(self._checksum, 1) + 38) & 0xFFFFFFFF

    def get_checksum(self):
        return struct.unpack('i', struct.pack('I', self._checksum))[0]

    def reset_checksum(self):
        self._checksum = 0

class ByteStream(ChecksumEncoder):
    def __init__(self, buffer=None):
        super().__init__()
        self.buffer = bytearray(buffer) if buffer else bytearray()
        self.offset = 0
        self.bit_idx = 0

    def read_boolean(self):
        if self.bit_idx == 0: self.offset += 1
        value = (self.buffer[self.offset - 1] & (1 << self.bit_idx)) != 0
        self.bit_idx = (self.bit_idx + 1) & 7
        return value

    def read_byte(self):
        self.bit_idx = 0
        val = self.buffer[self.offset]; self.offset += 1
        return val

    def read_int(self):
        self.bit_idx = 0
        val = struct.unpack_from('>i', self.buffer, self.offset)[0]
        self.offset += 4
        return val

    def read_vint(self):
        self.bit_idx = 0
        value = 0
        byte = self.buffer[self.offset]; self.offset += 1
        if (byte & 0x40) != 0:
            value |= byte & 0x3F
            if (byte & 0x80) == 0: return value | -64
            byte = self.buffer[self.offset]; self.offset += 1
            value |= (byte & 0x7F) << 6
            if (byte & 0x80) == 0: return value | -8192
            byte = self.buffer[self.offset]; self.offset += 1
            value |= (byte & 0x7F) << 13
            if (byte & 0x80) == 0: return value | -1048576
            byte = self.buffer[self.offset]; self.offset += 1
            value |= (byte & 0x7F) << 20
            if (byte & 0x80) == 0: return value | -134217728
            byte = self.buffer[self.offset]; self.offset += 1
            value |= (byte & 0x7F) << 27
            return value | -2147483648
        value |= byte & 0x3F
        if (byte & 0x80) == 0: return value
        byte = self.buffer[self.offset]; self.offset += 1
        value |= (byte & 0x7F) << 6
        if (byte & 0x80) == 0: return value
        byte = self.buffer[self.offset]; self.offset += 1
        value |= (byte & 0x7F) << 13
        if (byte & 0x80) == 0: return value
        byte = self.buffer[self.offset]; self.offset += 1
        value |= (byte & 0x7F) << 20
        if (byte & 0x80) == 0: return value
        byte = self.buffer[self.offset]; self.offset += 1
        value |= (byte & 0x7F) << 27
        return value

    def read_string(self):
        length = self.read_int()
        if length == -1: return None
        val = self.buffer[self.offset:self.offset+length].decode('utf-8')
        self.offset += length
        return val

    def ensure_capacity(self, capacity):
        if self.offset + capacity > len(self.buffer):
            self.buffer.extend([0] * (self.offset + capacity - len(self.buffer)))

    def write_boolean(self, value):
        super().write_boolean(value)
        if self.bit_idx == 0:
            self.ensure_capacity(1)
            self.buffer[self.offset] = 0
            self.offset += 1
        if value:
            self.buffer[self.offset - 1] |= (1 << self.bit_idx)
        self.bit_idx = (self.bit_idx + 1) & 7
        return value

    def write_byte(self, value):
        super().write_byte(value)
        self.ensure_capacity(1)
        self.bit_idx = 0
        self.buffer[self.offset] = value & 0xFF
        self.offset += 1
        return value

    def write_short(self, value):
        super().write_short(value)
        self.ensure_capacity(2)
        self.bit_idx = 0
        struct.pack_into('>h', self.buffer, self.offset, value)
        self.offset += 2

    def write_int(self, value):
        super().write_int(value)
        self.ensure_capacity(4)
        self.bit_idx = 0
        struct.pack_into('>i', self.buffer, self.offset, value)
        self.offset += 4

    def write_vint(self, value):
        super().write_vint(value)
        self.bit_idx = 0
        self.ensure_capacity(5)
        if value < 0:
            if value >= -64:
                self.buffer[self.offset] = (value & 0x3F) | 0x40; self.offset += 1
            elif value >= -8192:
                self.buffer[self.offset:self.offset+2] = [(value & 0x3F) | 0xC0, (value >> 6) & 0x7F]; self.offset += 2
            elif value >= -1048576:
                self.buffer[self.offset:self.offset+3] = [(value & 0x3F) | 0xC0, ((value >> 6) & 0x7F) | 0x80, (value >> 13) & 0x7F]; self.offset += 3
            elif value >= -134217728:
                self.buffer[self.offset:self.offset+4] = [(value & 0x3F) | 0xC0, ((value >> 6) & 0x7F) | 0x80, ((value >> 13) & 0x7F) | 0x80, (value >> 20) & 0x7F]; self.offset += 4
            else:
                self.buffer[self.offset:self.offset+5] = [(value & 0x3F) | 0xC0, ((value >> 6) & 0x7F) | 0x80, ((value >> 13) & 0x7F) | 0x80, ((value >> 20) & 0x7F) | 0x80, (value >> 27) & 0xF]; self.offset += 5
        else:
            if value < 64:
                self.buffer[self.offset] = value & 0x3F; self.offset += 1
            elif value < 8192:
                self.buffer[self.offset:self.offset+2] = [(value & 0x3F) | 0x80, (value >> 6) & 0x7F]; self.offset += 2
            elif value < 1048576:
                self.buffer[self.offset:self.offset+3] = [(value & 0x3F) | 0x80, ((value >> 6) & 0x7F) | 0x80, (value >> 13) & 0x7F]; self.offset += 3
            elif value < 134217728:
                self.buffer[self.offset:self.offset+4] = [(value & 0x3F) | 0x80, ((value >> 6) & 0x7F) | 0x80, ((value >> 13) & 0x7F) | 0x80, (value >> 20) & 0x7F]; self.offset += 4
            else:
                self.buffer[self.offset:self.offset+5] = [(value & 0x3F) | 0x80, ((value >> 6) & 0x7F) | 0x80, ((value >> 13) & 0x7F) | 0x80, ((value >> 20) & 0x7F) | 0x80, (value >> 27) & 0xF]; self.offset += 5
        return value

    def write_vlong(self, high, low):
        self.write_vint(high)
        self.write_vint(low)

    def write_bytes(self, value, length=-1):
        if length == -1: length = len(value) if value else 0
        super().write_bytes(value, length)
        self.bit_idx = 0
        if value is None:
            self.write_int(-1)
        else:
            self.write_int(length)
            self.ensure_capacity(length)
            self.buffer[self.offset:self.offset+length] = value
            self.offset += length

    def write_string(self, value):
        super().write_string(value)
        if value is None:
            self.write_int(-1)
        else:
            data = value.encode('utf-8')
            self.write_int(len(data))
            self.ensure_capacity(len(data))
            self.buffer[self.offset:self.offset+len(data)] = data
            self.offset += len(data)

    def write_string_reference(self, value):
        super().write_string_reference(value)
        if value is not None:
            self.write_string(value)
        else:
            self.write_int(0)

    def get_buffer(self):
        return bytes(self.buffer[:self.offset])

class LogicLong:
    def __init__(self, high=0, low=0):
        self.high = high
        self.low = low

    def encode(self, stream):
        # Default encode uses WriteInt for LoginOk compatibility
        stream.write_int(self.high)
        stream.write_int(self.low)
        return self

    def encode_vint(self, stream):
        stream.write_vint(self.high)
        stream.write_vint(self.low)
        return self
