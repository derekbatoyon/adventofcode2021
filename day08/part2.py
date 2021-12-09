#!/usr/local/bin/python3

import argparse
import fileinput
import sys

# wires
#    top
# ul     ur
#    mid
# ll     lr
#    bot

# top: 8 times
# ul:  6 times
# ur:  8 times
# mid: 7 times
# ll:  4 times
# lr:  9 times
# bot: 7 times

debug_level = 0

class Decoder:
    def __init__(self, signal_patterns):
        all_wires = set('abcdefg')

        signal_patterns = sorted(signal_patterns, key=lambda pattern: len(pattern))

        assert len(signal_patterns[0]) == 2
        one = set(signal_patterns[0])

        assert len(signal_patterns[1]) == 3
        seven = set(signal_patterns[1])

        assert len(signal_patterns[2]) == 4
        four = set(signal_patterns[2])

        assert len(signal_patterns[9]) == 7
        eight = set(signal_patterns[9])

        diff = seven - one
        assert len(diff) == 1
        top = diff.pop()

        # wires in four but not one either ul or mid
        for wire in four - one:
            count = sum(map(lambda pattern: wire in pattern, signal_patterns))
            if count == 6:
                ul = wire
            elif count == 7:
                mid = wire
            else:
                raise RuntimeError

        for pattern in signal_patterns[6:9]:
            assert len(pattern) == 6
            diff = eight.difference(pattern)
            assert len(diff) == 1
            wire = diff.pop()
            count = sum(map(lambda pattern: wire in pattern, signal_patterns))
            if count == 4:
                ll = wire
            elif count == 8:
                ur = wire
            elif count == 7:
                assert mid == wire
            else:
                raise RuntimeError

        remaining = all_wires.difference(top, ul, ur, mid, ll)
        assert len(remaining) == 2
        for wire in remaining:
            count = sum(map(lambda pattern: wire in pattern, signal_patterns))
            if count == 9:
                lr = wire
            elif count == 7:
                bot = wire
            else:
                raise RuntimeError

        if debug_level > 1:
            sys.stderr.write(' {} \n'.format(top * 4))
            sys.stderr.write('{}    {}\n'.format(ul, ur))
            sys.stderr.write('{}    {}\n'.format(ul, ur))
            sys.stderr.write(' {} \n'.format(mid * 4))
            sys.stderr.write('{}    {}\n'.format(ll, lr))
            sys.stderr.write('{}    {}\n'.format(ll, lr))
            sys.stderr.write(' {} \n'.format(bot * 4))

        zero = all_wires.difference(mid)
        two = all_wires.difference(ul, lr)
        three = all_wires.difference(ul, ll)
        six = all_wires.difference(ur)
        five = six.difference(ll)
        nine = all_wires.difference(ll)

        self.pattern_map = {
            ''.join(sorted(zero))  : 0,
            ''.join(sorted(one))   : 1,
            ''.join(sorted(two))   : 2,
            ''.join(sorted(three)) : 3,
            ''.join(sorted(four))  : 4,
            ''.join(sorted(five))  : 5,
            ''.join(sorted(six))   : 6,
            ''.join(sorted(seven)) : 7,
            ''.join(sorted(eight)) : 8,
            ''.join(sorted(nine))  : 9,
        }

    def decode(self, output_values):
        number = 0
        for value in output_values:
            pattern = ''.join(sorted(value))
            number = number * 10 + self.pattern_map[pattern]
        return number

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--debug', nargs='?', type=int, const=1, default=0)
    args = parser.parse_args()

    debug_level = args.debug

    total = 0

    input = fileinput.FileInput(files=args.files)
    for line in input:
        (signal_patterns_string, output_value_string) = line.split('|')
        signal_patterns = signal_patterns_string.strip().split()
        output_values = output_value_string.strip().split()

        decoder = Decoder(signal_patterns)
        number = decoder.decode(output_values)
        total += number

        if debug_level > 0:
            sys.stderr.write('{}: {}\n'.format(' '.join(output_values), number))

    print(total)
