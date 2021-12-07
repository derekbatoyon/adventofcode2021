#!/usr/local/bin/python3

import argparse
import fileinput

def hardcoded_fuel_cost(delta_p):
    return (delta_p * delta_p + delta_p) / 2

def total_fuel_cost(fuel_cost, positions, alignment):
    return sum(map(lambda p: int(fuel_cost(abs(p - alignment))), positions))

def determine_fuel_cost_function():
    import numpy
    def cost_generator():
        total = 0
        i = 0
        while True:
            total += i
            i += 1
            yield total

    x = numpy.arange(50)
    y_generator = cost_generator()
    y = [next(y_generator) for _ in x]
    return numpy.poly1d(numpy.polyfit(x, y, 2))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--hardcode', action='store_true')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)
    line = next(input)
    positions = [int(n) for n in line.split(',')]

    if args.hardcode:
        fuel_cost = hardcoded_fuel_cost
    else:
        fuel_cost = determine_fuel_cost_function()

    print(min([total_fuel_cost(fuel_cost, positions, alignment) for alignment in range(len(positions))]))
