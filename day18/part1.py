#!/usr/local/bin/python3

from copy import deepcopy

import argparse
import fileinput
import itertools
import math
import sys

def read_snailfish(input):
    if isinstance(input, str):
        return read_snailfish(iter(input))

    c = next(input)
    while c in ',]':
        c = next(input)

    if c == '[':
        value = SnailfishNumber(input)
    elif c.isdigit():
        value = int(c)
        for c in itertools.takewhile(lambda c: c.isdigit(), input):
            value = value * 10 + int(c)

    return value

class SnailfishNumber:
    class Explosion:
        def __init__(self, parent, node):
            self.parent = parent
            if node is self.parent.left:
                self.attr = 'left'
            if node is self.parent.right:
                self.attr = 'right'
        def do_explode(self):
            setattr(self.parent, self.attr, 0)

    class Number:
        def __init__(self, node, attr):
            self.node = node
            self.attr = attr
        def get(self):
            return getattr(self.node, self.attr)
        def add(self, value):
            setattr(self.node, self.attr, self.get() + value)
        def __repr__(self):
            return '{} ({})'.format(repr(self.node), self.get())

    auto_reduce = True

    def __init__(self, *args):
        if len(args) == 1:
            input = args[0]
            assert hasattr(input, '__iter__')
            self.left = read_snailfish(input)
            self.right = read_snailfish(input)
        else:
            self.left, self.right = args

    def __str__(self):
        return '[{},{}]'.format(self.left, self.right)

    def __add__(self, other):
        new_number = SnailfishNumber(deepcopy(self), deepcopy(other))
        new_number.reduce()
        return new_number

    def __eq__(self, other):
        if isinstance(self.left, SnailfishNumber) ^ isinstance(other.left, SnailfishNumber):
            return False
        elif isinstance(self.right, SnailfishNumber) ^ isinstance(other.right, SnailfishNumber):
            return False
        return self.left == other.left and self.right == other.right

    def reduce(self):
        if self.auto_reduce:
            while self.explode() or self.split():
                pass

    def explode(self):
        def search_nodes(node, parent=None, depth=1):
            if isinstance(node.left, SnailfishNumber):
                yield from search_nodes(node.left, node, depth+1)
            if isinstance(node.left, int):
                yield self.Number(node, 'left')
            if isinstance(node.left, int) and isinstance(node.right, int) and depth > 4:
                yield self.Explosion(parent, node)
            if isinstance(node.right, int):
                yield self.Number(node, 'right')
            if isinstance(node.right, SnailfishNumber):
                yield from search_nodes(node.right, node, depth+1)

        left_number = None
        left_value = None
        explosion = None
        search = search_nodes(self)
        for item in search:
            if isinstance(item, self.Explosion):
                explosion = item
                break
            assert isinstance(item, self.Number)
            left_number = left_value
            left_value = item

        if explosion:
            assert left_value is not None
            if left_number:
                left_number.add(left_value.get())
            try:
                right_value = next(search)
                right_number = next(search)
                right_number.add(right_value.get())
            except StopIteration:
                pass
            explosion.do_explode()
            return True

    def split(self):
        did_split = False
        if isinstance(self.left, SnailfishNumber):
            did_split = self.left.split()
        elif self.left > 9:
            value = self.left
            self.left = SnailfishNumber(math.floor(value/2), math.ceil(value/2))
            return True

        if not did_split:
            if isinstance(self.right, SnailfishNumber):
                did_split = self.right.split()
            elif self.right > 9:
                value = self.right
                self.right = SnailfishNumber(math.floor(value/2), math.ceil(value/2))
                return True

        return did_split

    def magnitude(self):
        if isinstance(self.left, SnailfishNumber):
            left = self.left.magnitude()
        else:
            left = self.left
        if isinstance(self.right, SnailfishNumber):
            right = self.right.magnitude()
        else:
            right = self.right
        return 3 * left + 2 * right

def test_explode(before, after):
    actual = read_snailfish(before)
    expected = read_snailfish(after)
    did_explode = actual.explode()
    assert did_explode
    assert actual == expected, 'expected: {} actual: {}'.format(expected, actual)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--show-steps', action='store_true')
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)

    if args.test:
        for line in input:
            snailfish = read_snailfish(line)
            print(snailfish)

        a = read_snailfish('[1,2]')
        b = read_snailfish('[[3,4],5]')
        c = read_snailfish('[[1,2],[[3,4],5]]')
        assert a + b == c

        test_explode('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]')
        test_explode('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]')
        test_explode('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]')
        test_explode('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
        test_explode('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[7,0]]]]')

        SnailfishNumber.auto_reduce = False
        a = read_snailfish('[[[[4,3],4],4],[7,[[8,4],9]]]')
        b = read_snailfish('[1,1]')
        c = read_snailfish('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]') # after addition
        d = read_snailfish('[[[[0,7],4],[7,[[8,4],9]]],[1,1]]')     # after explode
        e = read_snailfish('[[[[0,7],4],[15,[0,13]]],[1,1]]')       # after explode
        f = read_snailfish('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]')    # after split
        g = read_snailfish('[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]') # after split
        h = read_snailfish('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')     # after explode
        assert a + b == c
        did_explode = c.explode()
        assert did_explode
        assert c == d, 'expected: {} actual: {}'.format(d, c)
        did_explode = d.explode()
        assert did_explode
        assert d == e, 'expected: {} actual: {}'.format(e, d)
        did_split = e.split()
        assert did_split
        assert e == f, 'expected: {} actual: {}'.format(f, e)
        did_split = f.split()
        assert did_split
        assert f == g, 'expected: {} actual: {}'.format(g, f)
        did_explode = g.explode()
        assert did_explode
        assert g == h, 'expected: {} actual: {}'.format(h, g)

        a = read_snailfish('[9,1]')
        assert a.magnitude() == 29
        b = read_snailfish('[1,9]')
        assert b.magnitude() == 21
        c = read_snailfish('[[9,1],[1,9]]')
        assert c.magnitude() == 129
        d = read_snailfish('[[1,2],[[3,4],5]]')
        assert d.magnitude() == 143
        e = read_snailfish('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]')
        assert e.magnitude() == 1384
        f = read_snailfish('[[[[1,1],[2,2]],[3,3]],[4,4]]')
        assert f.magnitude() == 445
        g = read_snailfish('[[[[3,0],[5,3]],[4,4]],[5,5]]')
        assert g.magnitude() == 791
        h = read_snailfish('[[[[5,0],[7,4]],[5,5]],[6,6]]')
        assert h.magnitude() == 1137
        i = read_snailfish('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]')
        assert i.magnitude() == 3488

    else:
        first_line = next(input)
        sum = read_snailfish(first_line)
        for line in input:
            addend = read_snailfish(line)
            if args.show_steps:
                if first_line is None:
                    print()
                print('  {}'.format(sum))
                print('+ {}'.format(addend))
            sum = sum + addend
            if args.show_steps:
                print('= {}'.format(sum))
                first_line = None
        if not args.show_steps:
            sys.stderr.write('final sum: {}\n'.format(sum))
        print(sum.magnitude())
