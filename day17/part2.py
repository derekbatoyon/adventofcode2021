#!/usr/local/bin/python3

import argparse
import fileinput
import math
import re
import sys

global_debug = False

class Target:
    def __init__(self, x_min, x_max, y_bot, y_top):
        self.x_min = x_min
        self.x_max = x_max
        self.y_bot = y_bot
        self.y_top = y_top

    def hit_x(self, x):
        if x < self.x_min:
            return False
        if x > self.x_max:
            return False
        return True

    def hit_y(self, y):
        if y > self.y_top:
            return False
        if y < self.y_bot:
            return False
        return True

    def hit(self, x, y):
        return self.hit_x(x) and self.hit_y(y)

def quadratic_solve(a, b, c):
    discriminate = b**2-4*a*c
    divisor = 2*a
    if discriminate < 0:
        return []
    if discriminate == 0:
        return [-b / divisor]
    sqrt = math.sqrt(discriminate)
    return [(-b+sqrt) / divisor, (-b-sqrt) / divisor]

def calculate_minimum_x_velocity(x_min):
    solutions = list(filter(lambda x: x > 0, quadratic_solve(0.5, 0.5, -x_min)))
    assert len(solutions) > 0, 'You may have to fire backwards'
    return math.ceil(min(solutions))

def calculate_maximum_y(velocity):
    y = (velocity*velocity+velocity)/2
    assert math.ceil(y) == math.floor(y)
    return math.ceil(y)

def calculate_x(velocity, step):
    if step > velocity:
        step = velocity
    return int(-0.5*step*step + (velocity + 0.5)*step)

def x_positions(velocity, limit=None):
    x = 0
    yield x
    step = 1 if velocity > 0 else -1
    while limit is None or (x + velocity) <= limit:
        x += velocity
        if velocity != 0:
            velocity -= step
        yield x

def y_positions(velocity, limit=None):
    y = 0
    yield y
    while limit is None or (y + velocity) >= limit:
        y += velocity
        velocity -= 1
        yield y

def undershoot(target, x_velocity, y_velocity):
    # determine step at which probe will drop below target area
    solutions = list(filter(lambda s: s > 0, quadratic_solve(-0.5, y_velocity+0.5, -target.y_bot)))
    assert len(solutions) == 1
    step = math.floor(solutions.pop())

    # did probe reach target area
    return calculate_x(x_velocity, step) < target.x_min

def test_fire(target, x_velocity, y_velocity):
    return any(map(lambda x, y: target.hit(x, y), x_positions(x_velocity), y_positions(y_velocity, target.y_bot)))

def aim_probe(target):
    hits = 0

    min_x_velocity = calculate_minimum_x_velocity(target.x_min)
    max_x_velocity = target.x_max

    if global_debug:
        sys.stderr.write('x velocity range: {} to {}\n'.format(min_x_velocity, max_x_velocity))

    for x_velocity in range(min_x_velocity, max_x_velocity+1):
        y_velocity = abs(target.y_bot) - 1
        while not undershoot(target, x_velocity, y_velocity):
            hit = test_fire(target, x_velocity, y_velocity)
            if hit:
                hits += 1
            if global_debug:
                sys.stderr.write('{} {}: {}\n'.format(x_velocity, y_velocity, 'hit' if hit else 'miss'))

            y_velocity -= 1

    return hits

def draw(target, x_velocity, y_velocity, start_x=0, start_y=0):
    positions = list(zip(x_positions(x_velocity), y_positions(y_velocity, target.y_bot)))
    y_top = calculate_maximum_y(y_velocity)
    for y in range(max(start_y, y_top), target.y_bot-1, -1):
        for x in range(min(start_x, target.x_min), target.x_max+1):
            if x == start_x and y == start_y:
                sys.stderr.write('S')
            elif (x, y) in positions:
                sys.stderr.write('#')
            elif target.hit(x, y):
                sys.stderr.write('T')
            else:
                sys.stderr.write('.')
        sys.stderr.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    parser.add_argument('--test', type=int, nargs=2)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    global_debug = args.debug

    input_pattern = re.compile(r'target area: x=(?P<x_min>-?\d+)..(?P<x_max>-?\d+), y=(?P<y_bot>-?\d+)..(?P<y_top>-?\d+)')

    input = fileinput.FileInput(files=args.files)
    input_match = input_pattern.match(next(input))
    assert input_match

    x_min = int(input_match.group('x_min'))
    x_max = int(input_match.group('x_max'))
    y_bot = int(input_match.group('y_bot'))
    y_top = int(input_match.group('y_top'))
    target = Target(x_min, x_max, y_bot, y_top)

    if args.test:
        draw(target, args.test[0], args.test[1])
    else:
        print(aim_probe(target))
