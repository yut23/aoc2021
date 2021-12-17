import functools
import operator
from dataclasses import dataclass
from typing import List


class Stream:
    def __init__(self, data: str):
        self.data = bytes.fromhex(data)
        # bit offset of the beginning of the stream
        self.start = 0
        # current bit offset into data[start:]
        self.pos = 0
        self.length = len(self.data) * 8

    def __repr__(self) -> str:
        return f"Stream(data={self.data!r}, start={self.start}, length={self.length}, pos={self.pos})"

    @property
    def curr_bit(self) -> int:
        # offset in current byte: 0 is MSB or bit 7 (1<<7), 1 is bit 6, ..., 7 is bit 0 (1<<0=1)
        return (self.start + self.pos) % 8

    @property
    def curr_byte(self) -> int:
        # offset of current byte
        return (self.start + self.pos) // 8

    def read_bit(self) -> int:
        bit = 1 if self.data[self.curr_byte] & (1 << (7 - self.curr_bit)) else 0
        assert self.pos + 1 <= self.length, "Can't read past end of stream"
        self.pos += 1
        return bit

    def read_bits(self, count: int) -> int:
        val = 0
        for _ in range(count):
            val <<= 1
            val |= self.read_bit()
        return val

    def substream(self, length: int) -> "Stream":
        # construct the substream
        s = Stream("")
        s.data = self.data
        s.start = self.start + self.pos
        s.pos = 0
        s.length = length
        # advance this stream to after the substream
        assert self.pos + length <= self.length
        self.pos += length
        return s

    def read_literal(self) -> int:
        val = 0
        more = 1
        while more:
            more = self.read_bit()
            val <<= 4
            val |= self.read_bits(4)
        return val


@dataclass
class Packet:
    version: int
    type_id: int

    def get_value(self) -> int:
        return -1


@dataclass
class LiteralPacket(Packet):
    value: int

    def get_value(self) -> int:
        return self.value


@dataclass
class OperatorPacket(Packet):
    subpackets: List["Packet"]

    def get_value(self) -> int:
        op = {
            0: sum,
            1: lambda vals: functools.reduce(operator.mul, vals),
            2: min,
            3: max,
            5: lambda vals: operator.gt(*vals),
            6: lambda vals: operator.lt(*vals),
            7: lambda vals: operator.eq(*vals),
        }[self.type_id]
        subvalues = (p.get_value() for p in self.subpackets)
        return int(op(subvalues))  # type: ignore


def read_packet(s: Stream) -> Packet:
    version = s.read_bits(3)
    type_id = s.read_bits(3)

    if type_id == 4:
        return LiteralPacket(version, type_id, value=s.read_literal())
    # operator packet
    length_type_id = int(s.read_bit())
    if length_type_id == 0:
        # fixed length
        total_length = s.read_bits(15)
        packets = []
        substream = s.substream(total_length)
        # read packets until the end of the substream
        while substream.pos < total_length:
            packets.append(read_packet(substream))
        return OperatorPacket(version, type_id, subpackets=packets)
    # else:
    # fixed number of packets
    packet_count = s.read_bits(11)
    packets = [read_packet(s) for _ in range(packet_count)]
    return OperatorPacket(version, type_id, subpackets=packets)


def add_versions(packet: Packet) -> int:
    total = packet.version
    if isinstance(packet, OperatorPacket):
        for subpacket in packet.subpackets:
            total += add_versions(subpacket)
    return total


def part_1(lines: List[str]) -> int:
    stream = Stream(lines[0])
    packet = read_packet(stream)
    return add_versions(packet)


def part_2(lines: List[str]) -> int:
    stream = Stream(lines[0])
    packet = read_packet(stream)
    return packet.get_value()
