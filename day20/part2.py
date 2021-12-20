#!/usr/local/bin/python3

import argparse
import fileinput

pixel_translation = str.maketrans('.#', '01')

class Grid:
    def __init__(self, raw_data):
        raw_cols = len(raw_data[0])
        for row in raw_data[1:]:
            assert len(row) == raw_cols
        self.rows = len(raw_data) + 2
        self.cols = raw_cols + 2
        darkrow = list('.' * self.cols)
        self.grid = [darkrow.copy()]
        for raw_row in raw_data:
            self.grid.append(['.'] + raw_row + ['.'])
        self.grid.append(darkrow)

    def pixel(self, row, col):
        if row < 0:
            row = 0
        elif row >= self.rows:
            row = self.rows - 1
        if col < 0:
            col = 0
        elif col >= self.cols:
            col = self.cols - 1
        return self.grid[row][col]

    def sub_image_value(self, row, col):
        str = ''.join([self.pixel(r, c) for r in range(row-1,row+2) for c in range(col-1,col+2)])
        return int(str.translate(pixel_translation), base=2)

    def print(self, output, margin=None):
        if margin is None:
            row_range = range(self.rows)
            col_range = range(self.cols)
        else:
            row_range = range(-margin, self.rows+margin)
            col_range = range(-margin, self.cols+margin)
        for row in row_range:
            output.write('{}\n'.format(''.join([self.pixel(row, col) for col in col_range])))

    def process(self, algorithm):
        assert len(algorithm) == 512
        new_data = [[algorithm[self.sub_image_value(r, c)] for c in range(-2,self.cols+2)] for r in range(-2,self.rows+2)]
        self.grid = new_data
        self.rows = len(new_data)
        self.cols = len(new_data[0])

    def count_lit(self):
        return sum(map(lambda pixel: 0 if pixel == '.' else 1, [self.grid[r][c] for r in range(self.rows) for c in range(self.cols)]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()


    input = fileinput.FileInput(files=args.files)

    image_enhancement_algorithm = next(input).strip()
    blank_line = next(input).strip()
    assert len(blank_line) == 0

    data = [[c for c in line.strip()] for line in input]
    grid = Grid(data)

    for _ in range(50):
        grid.process(image_enhancement_algorithm)

    print(grid.count_lit())
