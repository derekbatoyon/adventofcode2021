#!/usr/local/bin/python3

import argparse
import fileinput

class Simulation:
    def __init__(self, input):
        self.grid = [[int(n) for n in line.strip()] for line in input]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        assert all(map(lambda row: len(row) == self.cols, self.grid[1:]))
        self.steps = 0

    def adjacents(self, row, col):
        above = row - 1
        below = row + 1
        left = col - 1
        right = col + 1

        if above >= 0:
            if left >= 0:
                yield (above, left)
            yield (above, col)
            if right < self.rows:
                yield (above, right)

        if left >= 0:
            yield (row, left)
        if right < self.rows:
            yield (row, right)

        if below < self.rows:
            if left >= 0:
                yield (below, left)
            yield (below, col)
            if right < self.rows:
                yield (below, right)

    def flash(self, flashes, row, col):
        if (row, col) not in flashes:
            flashes.add((row, col))
            for adjacent in self.adjacents(row, col):
                r, c = adjacent
                self.grid[r][c] += 1
                if self.grid[r][c] > 9:
                    self.flash(flashes, r, c)

    def step(self):
        self.steps += 1
        flashes = set()
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[row][col] += 1
                if self.grid[row][col] > 9:
                    self.flash(flashes, row, col)

        for flash in flashes:
            r, c = flash
            self.grid[r][c] = 0

        return len(flashes)

    def run(self):
        all_flashes = self.rows * self.cols
        while self.step() != all_flashes:
            pass

    def print(self):
        for row in self.grid:
            print(''.join([str(n) for n in row]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)
    sim = Simulation(input)
    sim.run()

    print(sim.steps)
