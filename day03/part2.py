#!/usr/local/bin/python3

import fileinput
import sys

class Node:
    def __init__(self, value=''):
        self.value = value
        self.weight = 0
        self.children = {}

    def add(self, str):
        if len(str):
            self.weight += 1
            c = str[0]
            assert c in ['0', '1'], 'What should I do with "{}"?\n'.format(c)
            if not c in self.children:
                self.children[c] = Node(c)
            self.children[c].add(str[1:])

    def search(self, reverse):
        if len(self.children) == 0:
            return self.value

        children = list(self.children.values())
        children.sort(key=lambda node: node.value, reverse=reverse)
        children.sort(key=lambda node: node.weight, reverse=reverse)
        return self.value + children[0].search(reverse)

class Tree:
    def __init__(self, input):
        self.tree = Node()
        for line in input:
            self.tree.add(line.strip())

    def evaluate_rating(self, reverse):
        rating_str = self.tree.search(reverse)
        return int(rating_str, base=2)

if __name__ == '__main__':
    tree = Tree(fileinput.FileInput())

    generator_rating = tree.evaluate_rating(False)
    scrubber_rating = tree.evaluate_rating(True)

    sys.stderr.write('oxygen generator rating: {0:012b} => {0}\n'.format(generator_rating))
    sys.stderr.write('CO2 scrubber rating:     {0:012b} => {0}\n'.format(scrubber_rating))

    print(generator_rating * scrubber_rating)
