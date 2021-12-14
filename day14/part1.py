#!/usr/local/bin/python3

import argparse
import fileinput
import re
import sys

class Polymerizer:
    def __init__(self, input):
        rule_pattern = re.compile(r'(\w\w)\s+->\s+(\w)')
        self.rules = dict([rule_pattern.match(line).group(1, 2) for line in input])

    def grow(self, polymer):
        def apply_rules(pair):
            if pair in self.rules:
                return self.rules[pair] + pair[1]
            else:
                return pair[1]
        new_polymer = map(apply_rules, [polymer[i-1:i+1] for i in range(1, len(polymer))])
        return polymer[0] + ''.join(new_polymer)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--steps', type=int, default=10)
    parser.add_argument('--show-growth', action='store_true')
    args = parser.parse_args()


    input = fileinput.FileInput(files=args.files)

    polymer = next(input).strip()

    blank_line = next(input).strip()
    assert len(blank_line) == 0

    polymerizer = Polymerizer(input)

    if args.show_growth:
        sys.stderr.write('Template:     {}\n'.format(polymer))

    for step in range(args.steps):
        polymer = polymerizer.grow(polymer)
        if args.show_growth:
            if step < 4:
                sys.stderr.write('After step {}: {}\n'.format(step+1, polymer))
            else:
                sys.stderr.write('After step {}: length = {}\n'.format(step+1, len(polymer)))

    counts = sorted([polymer.count(element) for element in set(polymer)])

    print(counts[-1] - counts[0])
