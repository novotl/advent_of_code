from functools import reduce
from typing import Callable, Iterable, TypeVar
from dataclasses import dataclass

from advent_of_code.runner import PuzzleTemplate
import operator


@dataclass
class Packet:
    version: int
    type_id: int

    def version_sum(self) -> int:
        return self.version


@dataclass
class LiteralPacket(Packet):
    _value: int

    def value(self) -> int:
        return self._value


@dataclass
class OperatorPacket(Packet):
    sub_packets: list[Packet]
    operation: Callable[[int, int], int]

    def version_sum(self) -> int:
        return sum(packet.version_sum() for packet in self.sub_packets) + self.version

    def value(self) -> int:
        return self.operation((packet.value() for packet in self.sub_packets))


T = TypeVar("T")

operations = {
    0: sum,
    1: lambda x: reduce(operator.mul, x, 1),
    2: min,
    3: max,
    5: lambda x: next(x) > next(x),
    6: lambda x: next(x) < next(x),
    7: lambda x: next(x) == next(x),
}


def next_n(iter: Iterable[T], n: int) -> Iterable[T]:
    return (next(iter) for _ in range(n))


def parse(it) -> Packet:
    version = int("".join(next_n(it, 3)), base=2)
    type_id = int("".join(next_n(it, 3)), base=2)

    if type_id == 4:
        # type ID 4 means the packet is a literal value
        value_buffer = []
        while True:
            group = "".join(next_n(it, 5))
            value_buffer.append(group[1:])
            if group[0] == "0":
                break
        value = int("".join(value_buffer), base=2)
        return LiteralPacket(version=version, type_id=type_id, _value=value)
    else:
        # any packet with a type ID other than 4 represents an operator
        length_type_id = int("".join(next_n(it, 1)), base=2)

        if length_type_id == 0:
            # If the length type ID is 0, then the next 15 bits are a number that represents
            # the total length in bits of the sub-packets contained by this packet.
            total_length_in_bits = int("".join(next_n(it, 15)), base=2)

            sub_packet_bits = next_n(it, total_length_in_bits)

            sub_packets = []
            while True:
                try:
                    sub_packets.append(parse(sub_packet_bits))
                except RuntimeError:
                    break

            return OperatorPacket(
                version=version,
                type_id=type_id,
                sub_packets=sub_packets,
                operation=operations[type_id],
            )
        else:
            # If the length type ID is 1, then the next 11 bits are a number that represents
            # the number of sub-packets immediately contained by this packet.
            number_of_immediate_subpackets = int("".join(next_n(it, 11)), base=2)

            sub_packets = [parse(it) for _ in range(number_of_immediate_subpackets)]
            return OperatorPacket(
                version=version,
                type_id=type_id,
                sub_packets=sub_packets,
                operation=operations[type_id],
            )


@dataclass
class Puzzle(PuzzleTemplate):
    packet: Packet

    @classmethod
    def from_lines(cls, lines: Iterable[str]) -> "Puzzle":
        line = lines[0].strip()
        bits = "".join(f"{int(hex_, base=16):04b}" for hex_ in line)

        return cls(packet=parse(iter(bits)))

    def task_one(self) -> int:
        print(self.packet)
        return self.packet.version_sum()

    def task_two(self) -> int:
        """
        >>> Puzzle.from_lines(["C200B40A82"]).task_two()
        3
        >>> Puzzle.from_lines(["04005AC33890"]).task_two()
        54
        >>> Puzzle.from_lines(["880086C3E88112"]).task_two()
        7
        >>> Puzzle.from_lines(["CE00C43D881120"]).task_two()
        9
        >>> Puzzle.from_lines(["D8005AC2A8F0"]).task_two()
        1
        >>> Puzzle.from_lines(["F600BC2D8F"]).task_two()
        0
        >>> Puzzle.from_lines(["9C005AC2F8F0"]).task_two()
        0
        >>> Puzzle.from_lines(["9C0141080250320F1802104A08"]).task_two()
        1
        """
        return self.packet.value()
