#!/usr/local/bin/python3

import argparse
import fileinput

def fuel_cost(positions, alignment):
    return sum(map(lambda p: abs(p - alignment), positions))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)
    line = next(input)
    positions = [int(n) for n in line.split(',')]

    print(min([fuel_cost(positions, alignment) for alignment in range(len(positions))]))
