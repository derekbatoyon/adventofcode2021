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

    def explore_basin(self, basin, point):
        row, col = point
        if self.heightmap[row][col] == 9:
            return

        basin.add(point)
        adjacents = set(self.adjacents(row, col))
        new_adjacents = adjacents.difference(basin)

        for adjacent in new_adjacents:
            self.explore_basin(basin, adjacent)

    def basin_size(self, point):
        basin = set()
        self.explore_basin(basin, point)
        return len(basin)

    def basin_sizes(self):
        for low_point in self.low_points():
            yield self.basin_size(low_point)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)
    heightmap = Heightmap(input)

    sizes = sorted(heightmap.basin_sizes())
    print(math.prod(sizes[-3:]))
