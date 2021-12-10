#!/usr/local/bin/python3

import argparse
import fileinput

complement = {
    ')' : '(',
    ']' : '[',
    '}' : '{',
    '>' : '<',
}

points = {
    ')' : 3,
    ']' : 57,
    '}' : 1197,
    '>' : 25137,
}

def score(line):
    first_character = line[0]
    stack = [first_character]
    for c in line[1:]:

        # if this is a closing character
        if c in complement.keys():
            if complement[c] == stack[-1]:
                stack.pop()
            else:
                return points[c]

        # if this is an opening character
        else:
            stack += [c]

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)
    print(sum([score(line) for line in input]))
