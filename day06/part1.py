#!/usr/local/bin/python3

import argparse
import fileinput
import functools
import sys

global_debug = False

def fish_count(state):
    day = 0
    day_label = 'day: '
    while True:
        day += 1
        new_fish = 0
        for i in range(len(state)):
            state[i] -= 1
            if state[i] < 0:
                new_fish += 1
                state[i] = 6
        state += [8] * new_fish

        if global_debug:
            sys.stderr.write('After {:3} {} {}\n'.format(day, day_label, ','.join(map(str, state))))
            day_label = 'days:'

        yield len(state)

@functools.lru_cache
def one_fish(state, days):
    count_generator = fish_count([state])
    for _ in range(days):
        count = next(count_generator)

    return count

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

    total = sum([one_fish(n, args.days) for n in initial_state])
    print(total)
