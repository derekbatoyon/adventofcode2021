#!/usr/local/bin/python3

from functools import lru_cache

import argparse
import fileinput
import re

def combine(dict1, dict2):
    keys = set(dict1.keys())
    keys.update(dict2.keys())
    return {key: dict1.get(key, 0) + dict2.get(key, 0) for key in keys}

class Polymerizer:
    def __init__(self, input):
        rule_pattern = re.compile(r'(\w\w)\s+->\s+(\w)')
        self.rules = dict([rule_pattern.match(line).group(1, 2) for line in input])

    @lru_cache(maxsize=1024)
    def grow_pair(self, e1, e2, steps):
        if steps:
            new_element = self.rules[e1 + e2]
            counts1 = self.grow_pair(e1, new_element, steps - 1)
            counts2 = self.grow_pair(new_element, e2, steps - 1)
            return combine(counts1, counts2)
        else:
            return {e2: 1}

    def measure_growth(self, polymer, steps):
        total_counts = {polymer[0] : 1}
        for i in range(1, len(polymer)):
            counts = self.grow_pair(polymer[i-1], polymer[i], steps)
            total_counts = combine(total_counts, counts)
        return total_counts

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--steps', type=int, default=40)
    args = parser.parse_args()


    input = fileinput.FileInput(files=args.files)

    polymer = next(input).strip()

    blank_line = next(input).strip()
    assert len(blank_line) == 0

    polymerizer = Polymerizer(input)

    counts = polymerizer.measure_growth(polymer, args.steps)
    counts = sorted(counts.values())

    print(counts[-1] - counts[0])
