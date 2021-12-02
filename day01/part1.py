#!/usr/local/bin/python3

import fileinput

def int_input():
    for line in fileinput.input():
        yield int(line)

if __name__ == '__main__':
    larger = 0
    depths = int_input()
    last_depth = next(depths)
    for depth in depths:
        if depth > last_depth:
            larger += 1
        last_depth = depth

    print(larger)
