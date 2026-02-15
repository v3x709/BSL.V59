import struct

class ByteStream:
    def __init__(self, buffer=None):
        if buffer is None:
            self.buffer = bytearray()
        else:
            self.buffer = bytearray(buffer)
        self.offset = 0
        self.bit_idx = 0

    def read_boolean(self):
        if self.bit_idx == 0:
            self.offset += 1
        value = (self.buffer[self.offset - 1] & (1 << self.bit_idx)) != 0
        self.bit_idx = (self.bit_idx + 1) & 7
        return value

    def read_byte(self):
        self.bit_idx = 0
        val = self.buffer[self.offset]
        self.offset += 1
        return val

    def read_int(self):
        self.bit_idx = 0
        val = struct.unpack_from('>i', self.buffer, self.offset)[0]
        self.offset += 4
        return val

    def read_short(self):
        self.bit_idx = 0
        val = struct.unpack_from('>h', self.buffer, self.offset)[0]
        self.offset += 2
        return val

    def read_vint(self):
        self.bit_idx = 0
        value = 0
        byte_value = self.buffer[self.offset]
        self.offset += 1

        if (byte_value & 0x40) != 0:
            value |= byte_value & 0x3F
            if (byte_value & 0x80) == 0:
                return value | -64 # 0xFFFFFFC0

            byte_value = self.buffer[self.offset]
            self.offset += 1
            value |= (byte_value & 0x7F) << 6
            if (byte_value & 0x80) == 0:
                return value | -8192 # 0xFFFFE000

            byte_value = self.buffer[self.offset]
            self.offset += 1
            value |= (byte_value & 0x7F) << 13
            if (byte_value & 0x80) == 0:
                return value | -1048576 # 0xFFF00000

            byte_value = self.buffer[self.offset]
            self.offset += 1
            value |= (byte_value & 0x7F) << 20
            if (byte_value & 0x80) == 0:
                return value | -134217728 # 0xF8000000

            byte_value = self.buffer[self.offset]
            self.offset += 1
            value |= (byte_value & 0x7F) << 27
            return value | -2147483648 # 0x80000000

        value |= byte_value & 0x3F
        if (byte_value & 0x80) == 0:
            return value

        byte_value = self.buffer[self.offset]
        self.offset += 1
        value |= (byte_value & 0x7F) << 6
        if (byte_value & 0x80) == 0:
            return value

        byte_value = self.buffer[self.offset]
        self.offset += 1
        value |= (byte_value & 0x7F) << 13
        if (byte_value & 0x80) == 0:
            return value

        byte_value = self.buffer[self.offset]
        self.offset += 1
        value |= (byte_value & 0x7F) << 20
        if (byte_value & 0x80) == 0:
            return value

        byte_value = self.buffer[self.offset]
        self.offset += 1
        value |= (byte_value & 0x7F) << 27
        return value

    def read_string(self, max_capacity=2048):
        length = self.read_int()
        if length == -1:
            return None
        if length > max_capacity:
            return None
        value = self.buffer[self.offset : self.offset + length].decode('utf-8')
        self.offset += length
        return value

    def write_boolean(self, value):
        if self.bit_idx == 0:
            self.buffer.append(0)
            self.offset += 1
        if value:
            self.buffer[self.offset - 1] |= (1 << self.bit_idx)
        self.bit_idx = (self.bit_idx + 1) & 7
        return value

    def write_byte(self, value):
        self.bit_idx = 0
        self.buffer.append(value & 0xFF)
        self.offset += 1

    def write_int(self, value):
        self.bit_idx = 0
        self.buffer.extend(struct.pack('>i', value))
        self.offset += 4

    def write_short(self, value):
        self.bit_idx = 0
        self.buffer.extend(struct.pack('>h', value))
        self.offset += 2

    def write_vint(self, value):
        self.bit_idx = 0

        if value < 0:
            if value >= -64:
                self.buffer.append((value & 0x3F) | 0x40)
                self.offset += 1
            elif value >= -8192:
                self.buffer.append((value & 0x3F) | 0xC0)
                self.buffer.append((value >> 6) & 0x7F)
                self.offset += 2
            elif value >= -1048576:
                self.buffer.append((value & 0x3F) | 0xC0)
                self.buffer.append(((value >> 6) & 0x7F) | 0x80)
                self.buffer.append((value >> 13) & 0x7F)
                self.offset += 3
            elif value >= -134217728:
                self.buffer.append((value & 0x3F) | 0xC0)
                self.buffer.append(((value >> 6) & 0x7F) | 0x80)
                self.buffer.append(((value >> 13) & 0x7F) | 0x80)
                self.buffer.append((value >> 20) & 0x7F)
                self.offset += 4
            else:
                self.buffer.append((value & 0x3F) | 0xC0)
                self.buffer.append(((value >> 6) & 0x7F) | 0x80)
                self.buffer.append(((value >> 13) & 0x7F) | 0x80)
                self.buffer.append(((value >> 20) & 0x7F) | 0x80)
                self.buffer.append((value >> 27) & 0xF)
                self.offset += 5
        else:
            if value < 64:
                self.buffer.append(value & 0x3F)
                self.offset += 1
            elif value < 8192:
                self.buffer.append((value & 0x3F) | 0x80)
                self.buffer.append((value >> 6) & 0x7F)
                self.offset += 2
            elif value < 1048576:
                self.buffer.append((value & 0x3F) | 0x80)
                self.buffer.append(((value >> 6) & 0x7F) | 0x80)
                self.buffer.append((value >> 13) & 0x7F)
                self.offset += 3
            elif value < 134217728:
                self.buffer.append((value & 0x3F) | 0x80)
                self.buffer.append(((value >> 6) & 0x7F) | 0x80)
                self.buffer.append(((value >> 13) & 0x7F) | 0x80)
                self.buffer.append((value >> 20) & 0x7F)
                self.offset += 4
            else:
                self.buffer.append((value & 0x3F) | 0x80)
                self.buffer.append(((value >> 6) & 0x7F) | 0x80)
                self.buffer.append(((value >> 13) & 0x7F) | 0x80)
                self.buffer.append(((value >> 20) & 0x7F) | 0x80)
                self.buffer.append((value >> 27) & 0xF)
                self.offset += 5

    def write_string(self, value):
        self.bit_idx = 0
        if value is None:
            self.write_int(-1)
        else:
            encoded = value.encode('utf-8')
            self.write_int(len(encoded))
            self.buffer.extend(encoded)
            self.offset += len(encoded)

    def write_string_reference(self, value):
        if value is not None:
            self.write_string(value)
        else:
            self.write_int(0)

    def get_buffer(self):
        return bytes(self.buffer)

    def reset_offset(self):
        self.offset = 0
        self.bit_idx = 0
