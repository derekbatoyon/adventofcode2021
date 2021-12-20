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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    input = fileinput.FileInput(files=args.files)

    numbers = [read_snailfish(line) for line in input]
    print(max([(a+b).magnitude() for a, b in itertools.permutations(numbers, 2)]))
