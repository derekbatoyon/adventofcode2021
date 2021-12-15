#!/usr/local/bin/python3

from functools import cache
from colored import attr

import argparse
import fileinput
import operator
import sys

size_factor = 5

class Cave:
    def __init__(self, input):
        def rows():
            for line in input:
                row = [int(c) for c in line.strip()]
                yield row
        self.risk_level = list(rows())
        self.rows = len(self.risk_level)
        self.cols = len(self.risk_level[0])
        for row in self.risk_level[1:]:
            assert self.cols == len(row)
        self.goal = (size_factor*self.rows-1, size_factor*self.cols-1)

    def adjacents(self, position):
        x, y = position
        below = x + 1
        if below < size_factor*self.rows:
            yield (below, y)
        right = y + 1
        if right < size_factor*self.cols:
            yield (x, right)

    risk_adjustment = list(range(10)) + list(range(1, 10)) * (size_factor * 2 - 2)
    def calculate_risk(self, position):
        x, y = position
        risk = self.risk_level[x % self.rows][y % self.cols]
        risk += int(x / self.rows) + int(y / self.cols)
        return Cave.risk_adjustment[risk]

    @cache
    def search_paths(self, position):
        local_risk = self.calculate_risk(position)

        if position == self.goal:
            return (local_risk, [position])

        def total_risk(p):
            (risk, path) = self.search_paths(p)
            risk += local_risk
            new_path = path.copy()
            new_path.append(position)
            return (risk, new_path)

        return min([total_risk(adj) for adj in self.adjacents(position)], key=operator.itemgetter(0))

    def lowest_risk(self):
        start = (0, 0)
        min_path = min([self.search_paths(adj) for adj in self.adjacents(start)])
        min_path[1].append(start)
        return min_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--show-path', action='store_true')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)

    cave = Cave(input)
    sys.setrecursionlimit(4000)
    min_risk, min_path = cave.lowest_risk()

    attr_str = {
        False : attr('reset'),
        True  : attr('bold'),
    }

    for x in range(size_factor*cave.rows):
        last_on_path = False
        for y in range(size_factor*cave.cols):
            position = (x, y)
            risk = cave.calculate_risk(position)
            on_path = position in min_path
            if on_path ^ last_on_path and args.show_path:
                sys.stderr.write('{}'.format(attr_str[on_path]))
            sys.stderr.write('{}'.format(risk))
            last_on_path = on_path
        sys.stderr.write('{}\n'.format(attr_str[False]))

    print(min_risk)
