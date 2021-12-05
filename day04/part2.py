#!/usr/local/bin/python3

import fileinput

board_dimension = 5
board_size = board_dimension * board_dimension

def empty(line):
    return len(line.strip()) == 0

def parse_boards(input):
    board = []
    for line in input:
        if empty(line):
            assert len(board) == board_size
            yield board
            board = []
        board += [int(n) for n in line.split()]
    assert len(board) == board_size
    yield board

def winner(board):
    def is_none(value):
        return value is None

    # check rows
    for row in range(0,board_size,board_dimension):
        if all(map(is_none, board[row:row+board_dimension])):
            return True

    # check columns
    for col in range(0,board_dimension):
        if all(map(is_none, board[col:board_size:5])):
            return True

def bingo():
    input = fileinput.FileInput()

    first_line = next(input)
    numbers = [int(n) for n in first_line.split(',')]

    second_line = next(input)
    assert empty(second_line)

    boards = list(parse_boards(input))

    for number in numbers:
        for i, board in enumerate(boards):
            if board is None:
                continue

            while True:
                try:
                    index = board.index(number)
                    board[index] = None
                except ValueError:
                    break

            if winner(board):
                last_score = sum(filter(None, board)) * number
                boards[i] = None

    return last_score

if __name__ == '__main__':
    result = bingo()
    print(result)
