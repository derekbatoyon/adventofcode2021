#!/usr/local/bin/python3

from functools import cache

import argparse
import curses
import fileinput
import operator
import sys
import time

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
        self.window = None

    def set_window(self, window):
        self.window = window
        if self.window:
            self.attr = { False: curses.color_pair(0), True:  curses.color_pair(1) | curses.A_BOLD }

    def draw(self, path=[]):
        if self.window:
            self.window.clear()

            for x in range(size_factor*self.rows):
                for y in range(size_factor*self.cols):
                    position = (x, y)
                    self.window.addch(x, y, self.calculate_risk_ch(position), self.attr[position in path])

            self.window.refresh()
            time.sleep(0.05)

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

    def calculate_risk_ch(self, position):
        return self.calculate_risk(position) + ord('0')

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
            self.draw(new_path)
            return (risk, new_path)

        return min([total_risk(adj) for adj in self.adjacents(position)], key=operator.itemgetter(0))

    def lowest_risk(self):
        start = (0, 0)
        min_path = min([self.search_paths(adj) for adj in self.adjacents(start)])
        min_path[1].append(start)
        return min_path

def main(stdscr, args):
    if stdscr:
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    input = fileinput.FileInput(files=args.files)

    cave = Cave(input)
    cave.set_window(stdscr)
    min_risk, min_path = cave.lowest_risk()
    cave.draw(min_path)

    if stdscr:
        stdscr.addstr(cave.rows, 0, '{}'.format(min_risk))
        stdscr.refresh()
        stdscr.getkey()

    return min_risk

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--show-path', action='store_true')
    args = parser.parse_args()

    sys.setrecursionlimit(4000)

    if args.show_path:
        try:
            print(curses.wrapper(main, args))
        except KeyboardInterrupt:
            sys.stderr.write('search interrupted\n')
    else:
        print(main(None, args))
