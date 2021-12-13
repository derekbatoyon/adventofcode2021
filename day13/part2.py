#!/usr/local/bin/python3

import argparse
import fileinput
import re
import sys

def build_dot_list(dot_generator):
    new_dots = []
    for dot in dot_generator:
        if dot not in new_dots:
            new_dots.append(dot)
    return new_dots

def fold_along_x(dots, pivot):
    def fold_x():
        for x, y in dots:
            if x > pivot:
                yield (2*pivot-x, y)
            else:
                yield (x, y)

    return build_dot_list(fold_x())

def fold_along_y(dots, pivot):
    def fold_y():
        for x, y in dots:
            if y > pivot:
                yield (x, 2*pivot-y)
            else:
                yield (x, y)
    return build_dot_list(fold_y())

def print_dots(dots):
    max_x = max([x for x, _ in dots])
    max_y = max([y for _, y in dots])

    for y in range(max_y+1):
        for x in range(max_x+1):
            if (x, y) in dots:
                sys.stderr.write('#')
            else:
                sys.stderr.write('.')
        sys.stderr.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    point_pattern = re.compile(r'(?P<x>\d+),(?P<y>\d+)')
    fold_pattern = re.compile(r'fold along (?P<axis>x|y)=(?P<value>\d+)')

    fold_along = {
        'x': fold_along_x,
        'y': fold_along_y,
    }

    dots = []

    input = fileinput.FileInput(files=args.files)

    while point := point_pattern.match(next(input)):
        x, y = point.group('x', 'y')
        dots.append((int(x), int(y)))

    for line in input:
        if fold := fold_pattern.match(line):
            axis, value = fold.group('axis', 'value')
            dots = fold_along[axis](dots, int(value))

    print_dots(dots)
