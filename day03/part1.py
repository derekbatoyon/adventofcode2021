#!/usr/local/bin/python3

import fileinput
import operator

boolean_map = { True: '1', False: '0' }
def convert(boolean_list):
    return int(''.join(map(lambda b: boolean_map[b], boolean_list)), base=2)

if __name__ == '__main__':
    input = fileinput.FileInput()
    first_line = next(input)
    accumulator = [int(c) for c in first_line.strip()]

    for line in input:
        accumulator = list(map(operator.add, accumulator, [int(c) for c in line.strip()]))

    threshold = input.lineno() / 2

    gamma = [count > threshold for count in accumulator]
    epsilon = [count < threshold for count in accumulator]
    assert all(map(operator.xor, gamma, epsilon)), "No most common bit; result unspecified"

    gamma_rate = convert(gamma)
    epsilon_rate = convert(epsilon)

    print('{} x {} = {}'.format(gamma_rate, epsilon_rate, gamma_rate * epsilon_rate))
