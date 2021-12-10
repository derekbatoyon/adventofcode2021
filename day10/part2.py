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
    '\n' : 0,
    '('  : 1,
    '['  : 2,
    '{'  : 3,
    '<'  : 4,
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
                return None

        # if this is an opening character
        else:
            stack += [c]

    total = 0
    stack.reverse()
    for c in stack:
        total = total * 5 + points[c]

    return total

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)
    scores = sorted(filter(None, [score(line) for line in input]))
    count = len(scores)
    assert count % 2 == 1
    print(scores[int(count/2)])
