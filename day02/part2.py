#!/usr/local/bin/python3

import fileinput
import re

class Submarine:
    def __init__(self):
        self.horizontal_position = 0
        self.depth = 0
        self.aim = 0

    def move_forward(self, x):
        self.horizontal_position += x
        self.depth += self.aim * x

    def move_down(self, x):
        self.aim += x

    def move_up(self, x):
        self.aim -= x

if __name__ == '__main__':
    submarine = Submarine()

    parser = re.compile(r'(?P<command>\w+)\s+(?P<x>\d+)$')

    move = {
        'forward' : Submarine.move_forward,
        'down'    : Submarine.move_down,
        'up'      : Submarine.move_up,
    }

    for line in fileinput.input():
        match = parser.match(line)
        assert match, 'unexpected input: ' + line
        move[match.group('command')](submarine, int(match.group('x')))

    print(submarine.horizontal_position * submarine.depth)
