#!/usr/local/bin/python3

import argparse
import fileinput
import itertools
import math

class ValuePacket:
    def __init__(self, val):
        self.val = val
    def value(self):
        return self.val

class SumPacket:
    def __init__(self, subs):
        self.subs = subs
    def value(self):
        return sum([sub.value() for sub in self.subs])

class ProductPacket:
    def __init__(self, subs):
        self.subs = subs
    def value(self):
        return math.prod([sub.value() for sub in self.subs])

class MinimumPacket:
    def __init__(self, subs):
        self.subs = subs
    def value(self):
        return min([sub.value() for sub in self.subs])

class MaximumPacket:
    def __init__(self, subs):
        self.subs = subs
    def value(self):
        return max([sub.value() for sub in self.subs])

class GreaterThanPacket:
    def __init__(self, subs):
        assert len(subs) == 2
        self.a = subs[0]
        self.b = subs[1]
    def value(self):
        return int(self.a.value() > self.b.value())

class LessThanPacket:
    def __init__(self, subs):
        assert len(subs) == 2
        self.a = subs[0]
        self.b = subs[1]
    def value(self):
        return int(self.a.value() < self.b.value())

class EqualToPacket:
    def __init__(self, subs):
        assert len(subs) == 2
        self.a = subs[0]
        self.b = subs[1]
    def value(self):
        return int(self.a.value() == self.b.value())

def packet_factory(type, *args):
    if type == 0:
        return SumPacket(*args)
    if type == 1:
        return ProductPacket(*args)
    if type == 2:
        return MinimumPacket(*args)
    if type == 3:
        return MaximumPacket(*args)
    if type == 4:
        return ValuePacket(*args)
    if type == 5:
        return GreaterThanPacket(*args)
    if type == 6:
        return LessThanPacket(*args)
    if type == 7:
        return EqualToPacket(*args)
    assert False

def bit_decoder(input):
    for line in input:
        for c in line.strip():
            n = int(c, base=16)
            for i in reversed(range(4)):
                yield (n >> i) & 1

def sub_packets(bit, length):
    bit_window = itertools.islice(bit, length)
    while True:
        try:
            packet = decode_packet(bit_window)
            yield packet
        except StopIteration:
            return

def decode_number(bitstream, length):
    bits = itertools.islice(bitstream, length)
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value

def decode_packet(bit):
    version = decode_number(bit, 3)
    type = decode_number(bit, 3)
    if type == 4:
        literal_value = 0
        last_group = False
        while not last_group:
            last_group = (next(bit) == 0)
            for _ in range(4):
                literal_value = (literal_value << 1) | next(bit)
        packet = packet_factory(type, literal_value)
    else:
        length_type = next(bit)
        if length_type == 0:
            length = decode_number(bit, 15)
            data = list(sub_packets(bit, length))
        else:
            subpacket_count = decode_number(bit, 11)
            data = [decode_packet(bit) for _ in range(subpacket_count)]
        packet = packet_factory(type, data)

    return packet

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)
    bitstream = bit_decoder(input)
    packet = decode_packet(bitstream)

    for extra in bitstream:
        assert extra == 0

    print(packet.value())
