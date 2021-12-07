#!/usr/local/bin/python3

import argparse
import fileinput
import sys

global_debug = False

def fish_count(state):
    while True:
        new_fish = state[0]
        state = state[1:] + [new_fish]
        state[6] += new_fish

        yield sum(state)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, default=18)
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('file', nargs='*')
    args = parser.parse_args()

    global_debug = args.debug

    line = next(fileinput.input(args.file))
    initial_state = [0] * 9
    for n in line.split(','):
        initial_state[int(n)] += 1

    if global_debug:
        sys.stderr.write('Initial state: {}\n'.format(','.join(map(str, initial_state))))

    counter = fish_count(initial_state)
    for _ in range(args.days):
        total = next(counter)
    print(total)
