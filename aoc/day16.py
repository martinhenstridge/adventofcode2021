from . import util


HEX_TO_BIN = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


class BitStream:
    __slots__ = ("bits", "curr")

    def __init__(self, bits):
        self.bits = bits
        self.curr = 0

    def read(self, n):
        prev = self.curr
        self.curr += n
        return self.bits[prev : self.curr]

    def readint(self, n):
        return int(self.read(n), 2)

    def empty(self):
        return self.curr == len(self.bits)


class Packet:
    __slots__ = ("version", "type_id", "value", "subpackets")

    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id
        self.value = None
        self.subpackets = []

    def sum_versions(self):
        return self.version + sum(p.sum_versions() for p in self.subpackets)

    def evaluate(self):
        if self.type_id == 0:
            return self._evaluate_sum()
        if self.type_id == 1:
            return self._evaluate_product()
        if self.type_id == 2:
            return self._evaluate_minimum()
        if self.type_id == 3:
            return self._evaluate_maximum()
        if self.type_id == 4:
            return self._evaluate_literal()
        if self.type_id == 5:
            return self._evaluate_greater_than()
        if self.type_id == 6:
            return self._evaluate_less_than()
        if self.type_id == 7:
            return self._evaluate_equal_to()

    def _evaluate_sum(self):
        return sum(p.evaluate() for p in self.subpackets)

    def _evaluate_product(self):
        return util.product(p.evaluate() for p in self.subpackets)

    def _evaluate_minimum(self):
        return min(p.evaluate() for p in self.subpackets)

    def _evaluate_maximum(self):
        return max(p.evaluate() for p in self.subpackets)

    def _evaluate_literal(self):
        return self.value

    def _evaluate_greater_than(self):
        if self.subpackets[0].evaluate() > self.subpackets[1].evaluate():
            return 1
        return 0

    def _evaluate_less_than(self):
        if self.subpackets[0].evaluate() < self.subpackets[1].evaluate():
            return 1
        return 0

    def _evaluate_equal_to(self):
        if self.subpackets[0].evaluate() == self.subpackets[1].evaluate():
            return 1
        return 0


def get_transmission(lines):
    bits = "".join(HEX_TO_BIN[char] for line in lines for char in line)
    return BitStream(bits)


def parse_literal(bitstream):
    chunks = []
    more = True
    while more:
        more = bitstream.readint(1)
        chunk = bitstream.read(4)
        chunks.append(chunk)
    return int("".join(chunks), 2)


def parse_operator(bitstream):
    length_type_id = bitstream.read(1)

    if length_type_id == "0":
        length = bitstream.readint(15)
        substream = BitStream(bitstream.read(length))
        return parse_packets(substream)
    else:
        count = bitstream.readint(11)
        return [parse_packet(bitstream) for _ in range(count)]


def parse_packet(bitstream):
    version = bitstream.readint(3)
    type_id = bitstream.readint(3)
    packet = Packet(version, type_id)

    if type_id == 4:
        packet.value = parse_literal(bitstream)
    else:
        packet.subpackets = parse_operator(bitstream)

    return packet


def parse_packets(bitstream):
    packets = []
    while not bitstream.empty():
        packet = parse_packet(bitstream)
        packets.append(packet)
    return packets


def run():
    inputlines = util.get_input_lines("16.txt")

    bitstream = get_transmission(inputlines)
    packet = parse_packet(bitstream)

    return packet.sum_versions(), packet.evaluate()
