import requests


class Sudoku:
    def __init__(self):
        r = requests.get('https://sugoku.herokuapp.com/board?difficulty=easy')
        self.board = r.json()['board']
        print(self.board)

