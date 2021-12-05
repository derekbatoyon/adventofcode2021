#!/usr/local/bin/python3

import fileinput
import math
import operator
import sys

def evaluate_rating(numbers, select_one_op):
    max_value = max(numbers)
    bit_count = int((math.log(max_value, 2)))

    candidates = len(numbers)
    rating = 0

    for bit_position in range(bit_count, -1, -1):
        threshold = rating | 2 ** bit_position
        zero_count = sum(map(lambda n: rating <= n and n < threshold, numbers))
        one_count = candidates - zero_count

        if one_count == 0:
            # keep values with a 0 in the position
            candidates = zero_count
        elif zero_count == 0 or select_one_op(zero_count, one_count):
            # keep values with a 1 in the position
            rating = threshold
            candidates = one_count
        else:
            # keep values with a 0 in the position
            candidates = zero_count

    assert candidates == 1
    return rating

if __name__ == '__main__':
    numbers = [int(line, base=2) for line in fileinput.input()]

    generator_rating = evaluate_rating(numbers, operator.gt)
    scrubber_rating = evaluate_rating(numbers, operator.le)

    sys.stderr.write('oxygen generator rating: {0:012b} => {0}\n'.format(generator_rating))
    sys.stderr.write('CO2 scrubber rating:     {0:012b} => {0}\n'.format(scrubber_rating))

    print(generator_rating * scrubber_rating)
