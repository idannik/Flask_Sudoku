from contextlib import suppress

from flask import session
def init_board_options(board):
    options = []
    for i in range(9):
        row = []
        for j in range(9):
            val = set()
            if not board[i][j]:
                val = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            row.append(val)
        options.append(row)
    for i in range(9):
        for j in range(9):
            if board[i][j]:
                update_board_options_according_to_value(options, i, j, val=board[i][j])

    return options


def update_board_options_according_to_value(options, row, col, val):
    if val == 0:
        return
    for i in range(9):
            options[i][col].discard(val)
            options[row][i].discard(val)
    square_start_row = row - (row % 3)
    square_start_col = col - (col % 3)
    for i in range(3):
        for j in range(3):
            options[square_start_row + i][square_start_col + j].discard(val)

def find_next_move(board, options):
    res = find_lone_single(board, options)
    if res:
        return {
            'reason': 'lone_single',
            'pos': res[0],
            'value': res[1]
        }
    return {}

def find_lone_single(board, options):
    for i in range(9):
        for j in range(9):
            if len(options[i][j]) == 1:
                value = next(iter(options[i][j]))
                return (i, j), value
    return None
