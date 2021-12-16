#!/usr/local/bin/python3

import argparse
import fileinput
import itertools

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
    packet = {'version': version}

    type = decode_number(bit, 3)
    if type == 4:
        literal_value = 0
        last_group = False
        while not last_group:
            last_group = (next(bit) == 0)
            for _ in range(4):
                literal_value = (literal_value << 1) | next(bit)
        packet['type'] = 'literal'
        packet['value'] = literal_value
    else:
        length_type = next(bit)
        if length_type == 0:
            length = decode_number(bit, 15)
            data = list(sub_packets(bit, length))
        else:
            subpacket_count = decode_number(bit, 11)
            data = [decode_packet(bit) for _ in range(subpacket_count)]

        packet['type'] = 'operator'
        packet['value'] = data

    return packet

def extract_versions(packet):
    yield packet['version']
    if packet['type'] == 'operator':
        for sub_packet in packet['value']:
            yield from extract_versions(sub_packet)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)
    bitstream = bit_decoder(input)
    packet = decode_packet(bitstream)

    for extra in bitstream:
        assert extra == 0

    print(sum(extract_versions(packet)))
