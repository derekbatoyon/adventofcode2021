#!/usr/local/bin/python3

import argparse
import fileinput
import math

class Heightmap:
    def __init__(self, input):
        self.heightmap = [[int(n) for n in line.strip()] for line in input]
        self.rows = len(self.heightmap)
        self.cols = len(self.heightmap[0])
        assert all(map(lambda row: len(row) == self.cols, self.heightmap[1:]))

    def adjacents(self, row, col):
        above = row - 1
        if above >= 0:
            yield (above, col)

        left = col - 1
        if left >= 0:
            yield (row, left)

        below = row + 1
        if below < self.rows:
            yield (below, col)

        right = col + 1
        if right < self.cols:
            yield (row, right)

    def point_height(self, point):
        row, col = point
        return self.heightmap[row][col]

    def low_points(self):
        for row in range(self.rows):
            for col in range(self.cols):
                height = self.heightmap[row][col]
                adjacents = self.adjacents(row, col)
                if all(map(lambda h: h > height, [self.point_height(point) for point in adjacents])):
                    yield (row, col)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)
    heightmap = Heightmap(input)

    print(sum(map(lambda p: heightmap.point_height(p) + 1, heightmap.low_points())))
