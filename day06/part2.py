#!/usr/local/bin/python3

import argparse
import fileinput
import sys

global_debug = False

def fish_count():
    state = [0, 0, 0, 0, 0, 0, 1, 0, 0]
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
    initial_state = [int(n) for n in line.split(',')]

    if global_debug:
        sys.stderr.write('Initial state: {}\n'.format(','.join(map(str, initial_state))))

    counter = fish_count()
    for _ in range(1, args.days):
        next(counter)
    counts = [next(counter) for i in range(7)]
    total = sum([counts[6-n] for n in initial_state])
    print(total)
