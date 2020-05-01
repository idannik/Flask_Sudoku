import requests
from bs4 import BeautifulSoup


class Sudoku:
    def __init__(self):
        level = 'beginner'
        r = requests.get(f'http://www.sudoku-online.co.il/sudoku-print.php?id=4500').text
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







