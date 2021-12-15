#!/usr/local/bin/python3

from functools import cache

import argparse
import fileinput

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
        self.goal = (self.rows-1, self.cols-1)

    def adjacents(self, position):
        x, y = position
        below = x + 1
        if below < self.rows:
            yield (below, y)
        right = y + 1
        if right < self.cols:
            yield (x, right)

    @cache
    def search_paths(self, position):
        x, y = position
        risk = self.risk_level[x][y]

        if position == self.goal:
            return risk

        def total_risk(p):
            return risk + self.search_paths(p)

        return min([total_risk(adj) for adj in self.adjacents(position)])

    def lowest_risk(self):
        start = (0, 0)
        return min([self.search_paths(adj) for adj in self.adjacents(start)])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)

    cave = Cave(input)
    print(cave.lowest_risk())
