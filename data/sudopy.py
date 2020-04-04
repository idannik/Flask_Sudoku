import requests


class Sudoku:
    def __init__(self):
        level = 'easy'
        r = requests.get(f'https://sugoku.herokuapp.com/board?difficulty={level}')
        self.board = r.json()['board']


