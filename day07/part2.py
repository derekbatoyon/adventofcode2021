#!/usr/local/bin/python3

import argparse
import fileinput

def fuel_cost(delta_p):
    return int((delta_p * delta_p + delta_p) / 2)

def total_fuel_cost(positions, alignment):
    return sum(map(lambda p: fuel_cost(abs(p - alignment)), positions))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)
    line = next(input)
    positions = [int(n) for n in line.split(',')]

    print(min([total_fuel_cost(positions, alignment) for alignment in range(len(positions))]))
