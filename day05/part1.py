#!/usr/local/bin/python3

import fileinput
import re
import sys

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

    def __str__(self):
        return '{},{} -> {},{}'.format(self.x1, self.y1, self.x2, self.y2)

    def all_points(self):
        if self.x1 == self.x2:
            start_y = min(line.y1, line.y2)
            end_y   = max(line.y1, line.y2)
            for y in range(start_y, end_y+1):
                yield (self.x1, y)
        elif self.y1 == self.y2:
            start_x = min(line.x1, line.x2)
            end_x   = max(line.x1, line.x2)
            for x in range(start_x, end_x+1):
                yield (x, self.y1)

def parse_lines():
    line_pattern = re.compile(r'(\d+),(\d+)\s+->\s+(\d+),(\d+)')
    for line in fileinput.input():
        line_match = line_pattern.match(line)
        yield Line(*line_match.group(1, 2, 3, 4))

def print_points(point_list):
    max_x = max(point_list.keys()) + 1
    max_y = max([max(values) for values in point_list.values()]) + 1

    for y in range(0, max_y):
        for x in range(0, max_x):
            values = point_list.get(x, {})
            value = values.get(y, 0)
            if value == 0:
                sys.stderr.write('.')
            elif value > 9:
                sys.stderr.write('*')
            else:
                sys.stderr.write('{}'.format(value))
        sys.stderr.write('\n')

if __name__ == '__main__':
    point_list = {}
    for line in parse_lines():
        for x, y in line.all_points():
            if x not in point_list:
                point_list[x] = {}
            value = point_list[x].get(y, 0)
            point_list[x][y] = value + 1

    print_points(point_list)

    count = 0
    for values in point_list.values():
        for value in values.values():
            if value > 1:
                count += 1

    print(count)
