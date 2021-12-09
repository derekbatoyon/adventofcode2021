#!/usr/local/bin/python3

import argparse
import fileinput

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    counts = [
        0,
        0,
        0, # ones
        0, # threes
        0, # fours
        0,
        0,
        0  # eights
    ]

    input = fileinput.FileInput(files=args.files)
    for line in input:
        (_, output_value_string) = line.split('|')
        output_values = output_value_string.strip().split()
        for value in output_values:
            counts[len(value)] += 1

    counts[0] = counts[1] = counts[5] = counts[6] = 0
    print(sum(counts))
