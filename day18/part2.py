#!/usr/local/bin/python3

from functools import partial

import argparse
import fileinput
import itertools
import math
import re
import sys

number_pattern = re.compile(r'\b\d+\b')

def add(a, b, auto_reduce=True):
    snailfish = '[{},{}]'.format(a,b)
    if auto_reduce:
        snailfish = reduce(snailfish)
    return snailfish

def reduce(snailfish):
    did_explode, did_split = True, True
    while did_explode or did_split:
        snailfish, did_explode = explode(snailfish)
        if not did_explode:
            snailfish, did_split = split(snailfish)
    return snailfish

def explode(snailfish):
    def add_value(match, addend):
        return str(int(match.group(0)) + addend)
    def last(iter):
        last_item = None
        for item in iter:
            last_item = item
        return last_item

    explosion_start, explosion_end = None, None
    nest = 0
    for i, c in enumerate(snailfish):
        if c == '[':
            nest += 1
            if nest > 4:
                explosion_start = i
        elif c == ']':
            nest -= 1
            if explosion_start is not None:
                explosion_end = i + 1
                break

    if explosion_start is not None:
        assert explosion_end is not None, 'Invalid Snailfish number: {}'.format(snailfish)
        left_value, right_value = eval(snailfish[explosion_start:explosion_end])
        left_string = snailfish[:explosion_start]
        right_string = snailfish[explosion_end:]
        if match := last(number_pattern.finditer(left_string)):
            left_string = '{}{}{}'.format(left_string[:match.start()], add_value(match, addend=left_value), left_string[match.end():])
        right_string = number_pattern.sub(partial(add_value, addend=right_value), right_string, count=1)
        return ('{}0{}'.format(left_string, right_string), True)

    return (snailfish, False)

def split(snailfish):
    for match in number_pattern.finditer(snailfish):
        value = int(match.group())
        if value > 9:
            return ('{}[{},{}]{}'.format(snailfish[:match.start()], math.floor(value/2), math.ceil(value/2), snailfish[match.end():]), True)
    return (snailfish, False)

def magnitude(snailfish):
    def _magnitude(list_):
        left, right = list_
        if isinstance(left, list):
            left = _magnitude(left)
        if isinstance(right, list):
            right = _magnitude(right)
        return 3 * left + 2 * right
    return _magnitude(eval(snailfish))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)

    numbers = [line.strip() for line in input]
    print(max([magnitude(add(a, b)) for a, b in itertools.permutations(numbers, 2)]))
