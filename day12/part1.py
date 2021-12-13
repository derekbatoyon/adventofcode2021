#!/usr/local/bin/python3

import argparse
import fileinput

class CaveSystem:
    def __init__(self, input):
        self.cave = {}
        for line in input:
            (p1, p2) = line.strip().split('-')
            self.add_segment(p1, p2)
            self.add_segment(p2, p1)

    def add_segment(self, p1, p2):
        if p1 in self.cave:
            self.cave[p1].append(p2)
        else:
            self.cave[p1] = [p2]

    def next_caves(self, path):
        current_cave = path[-1]
        single_use_caves = list(filter(lambda pt: pt.islower(), path))
        for adjacent in self.cave[current_cave]:
            if adjacent not in single_use_caves:
                yield adjacent

    def follow_path(self, path):
        for next_cave in self.next_caves(path):
            new_path = path + [next_cave]
            if next_cave == 'end':
                yield ','.join(new_path)
            else:
                yield from self.follow_path(new_path)

    def paths(self):
        yield from self.follow_path(['start'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--show-paths', action='store_true')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)
    cave_system = CaveSystem(input)
    paths = cave_system.paths()

    if args.show_paths:
        for path in paths:
            print(path)
    else:
        print(len(list(paths)))
