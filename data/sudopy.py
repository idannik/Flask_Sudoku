import random

import requests
from bs4 import BeautifulSoup

sudoku_boards = {
    'easy': {
        'min': 1000,
        'max':  1977
    },
    'medium': {
        'min': 2000,
        'max':  2590
    },
    'hard': {
        'min': 3000,
        'max':  3484
    },
    'extra_hard': {
        'min': 4000,
        'max':  4722
    }

}

LEVEL = "medium"

def get_a_random_board(level='easy'):
    min = sudoku_boards[level]['min']
    max = sudoku_boards[level]['max']
    return random.randint(min, max)

class Sudoku:
    def __init__(self):
        # board = get_a_random_board(LEVEL)
        # board = 2582
        board = 4665
        print(f'Picked {LEVEL} board: {board}')
        r = requests.get(f'http://www.sudoku-online.co.il/sudoku-print.php?id=3400').text
        soup = BeautifulSoup(r, 'lxml')
        self.board = [[0] * 9 for _ in range(9)]
        for square_num, square in enumerate(soup.body.table.find_all('table')[1:]):
            square_row = square_num // 3
            square_col = square_num % 3
            for cell_num, cell in enumerate(square.children):
                cell_row = square_row*3 + (cell_num // 3)
                cell_col = square_col*3 + (cell_num % 3)
                if not cell.input:
                    self.board[cell_row][cell_col] = cell.contents[0]







