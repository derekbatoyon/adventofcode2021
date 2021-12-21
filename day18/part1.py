#!/usr/local/bin/python3

from functools import partial

import argparse
import fileinput
import math
import re
import sys

number_pattern = re.compile(r'\b\d+\b')

def add(a, b, auto_reduce=True):
    snailfish = '[{},{}]'.format(a,b)
    if auto_reduce:
        snailfish = reduce(snailfish)
    return snailfish

def reduce(snailfish):
    did_explode, did_split = True, True
    while did_explode or did_split:
        snailfish, did_explode = explode(snailfish)
        if not did_explode:
            snailfish, did_split = split(snailfish)
    return snailfish

def explode(snailfish):
    def add_value(match, addend):
        return str(int(match.group(0)) + addend)
    def last(iter):
        last_item = None
        for item in iter:
            last_item = item
        return last_item

    explosion_start, explosion_end = None, None
    nest = 0
    for i, c in enumerate(snailfish):
        if c == '[':
            nest += 1
            if nest > 4:
                explosion_start = i
        elif c == ']':
            nest -= 1
            if explosion_start is not None:
                explosion_end = i + 1
                break

    if explosion_start is not None:
        assert explosion_end is not None, 'Invalid Snailfish number: {}'.format(snailfish)
        left_value, right_value = eval(snailfish[explosion_start:explosion_end])
        left_string = snailfish[:explosion_start]
        right_string = snailfish[explosion_end:]
        if match := last(number_pattern.finditer(left_string)):
            left_string = '{}{}{}'.format(left_string[:match.start()], add_value(match, addend=left_value), left_string[match.end():])
        right_string = number_pattern.sub(partial(add_value, addend=right_value), right_string, count=1)
        return ('{}0{}'.format(left_string, right_string), True)

    return (snailfish, False)

def split(snailfish):
    for match in number_pattern.finditer(snailfish):
        value = int(match.group())
        if value > 9:
            return ('{}[{},{}]{}'.format(snailfish[:match.start()], math.floor(value/2), math.ceil(value/2), snailfish[match.end():]), True)
    return (snailfish, False)

def magnitude(snailfish):
    def _magnitude(list_):
        left, right = list_
        if isinstance(left, list):
            left = _magnitude(left)
        if isinstance(right, list):
            right = _magnitude(right)
        return 3 * left + 2 * right
    return _magnitude(eval(snailfish))

def test_explode(before, after):
    exploded, did_explode = explode(before)
    assert did_explode
    assert exploded == after, 'expected: {} actual: {}'.format(after, exploded)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--show-steps', action='store_true')
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)

    if args.test:
        a = '[1,2]'
        b = '[[3,4],5]'
        c = '[[1,2],[[3,4],5]]'
        assert add(a, b, auto_reduce=False) == c

        test_explode('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]')
        test_explode('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]')
        test_explode('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]')
        test_explode('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
        test_explode('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[7,0]]]]')

        a = '[[[[4,3],4],4],[7,[[8,4],9]]]'
        b = '[1,1]'
        c = '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]' # after addition
        d = '[[[[0,7],4],[7,[[8,4],9]]],[1,1]]'     # after explode
        e = '[[[[0,7],4],[15,[0,13]]],[1,1]]'       # after explode
        f = '[[[[0,7],4],[[7,8],[0,13]]],[1,1]]'    # after split
        g = '[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]' # after split
        h = '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'     # after explode
        assert add(a, b, auto_reduce=False) == c
        c, did_explode = explode(c)
        assert did_explode
        assert c == d, 'expected: {} actual: {}'.format(d, c)
        d, did_explode = explode(d)
        assert did_explode
        assert d == e, 'expected: {} actual: {}'.format(e, d)
        e, did_split = split(e)
        assert did_split
        assert e == f, 'expected: {} actual: {}'.format(f, e)
        f, did_split = split(f)
        assert did_split
        assert f == g, 'expected: {} actual: {}'.format(g, f)
        g, did_explode = explode(g)
        assert did_explode
        assert g == h, 'expected: {} actual: {}'.format(h, g)

        assert magnitude('[9,1]') == 29
        assert magnitude('[1,9]') == 21
        assert magnitude('[[9,1],[1,9]]') == 129
        assert magnitude('[[1,2],[[3,4],5]]') == 143
        assert magnitude('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]') == 1384
        assert magnitude('[[[[1,1],[2,2]],[3,3]],[4,4]]') == 445
        assert magnitude('[[[[3,0],[5,3]],[4,4]],[5,5]]') == 791
        assert magnitude('[[[[5,0],[7,4]],[5,5]],[6,6]]') == 1137
        assert magnitude('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]') == 3488

    else:
        first_line = True
        sum = next(input).strip()
        for line in input:
            addend = line.strip()
            if args.show_steps:
                if first_line is None:
                    print()
                print('  {}'.format(sum))
                print('+ {}'.format(addend))
            sum = add(sum, addend)
            if args.show_steps:
                print('= {}'.format(sum))
                first_line = None
        if not args.show_steps:
            sys.stderr.write('final sum: {}\n'.format(sum))
        print(magnitude(sum))
