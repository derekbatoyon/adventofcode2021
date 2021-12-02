#!/usr/local/bin/python3

import fileinput

def int_input():
    for line in fileinput.input():
        yield int(line)

def window_sum(iter, size=3):
    if size > 1:
        n = size - 1
        window = []
        while len(window) < n:
            window.append(next(iter))
        for it in iter:
            window.append(it)
            yield sum(window)
            window.pop(0)

def main():
    larger = 0
    depths = window_sum(int_input())
    last_depth = next(depths)
    for depth in depths:
        if depth > last_depth:
            larger += 1
        last_depth = depth

    print(larger)

if __name__ == '__main__':
    main()
