#!/usr/local/bin/python3

import argparse
import fileinput

def adjacents(heightmap, row, col):
    above = row-1
    if above >= 0:
        yield heightmap[above][col]

    left = col - 1
    if left >= 0:
        yield heightmap[row][left]

    try:
        yield heightmap[row+1][col]
    except IndexError:
        pass

    try:
        yield heightmap[row][col+1]
    except IndexError:
        pass

def low_points(heightmap):
    for row in range(len(heightmap)):
        for col in range(len(heightmap[row])):
            height = heightmap[row][col]
            adjacent_height = list(adjacents(heightmap, row, col))
            if all(map(lambda h: h > height, adjacent_height)):
                yield height

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)
    heightmap = [[int(n) for n in line.strip()] for line in input]
    print(sum(map(lambda h: h + 1, low_points(heightmap))))
