from copy import deepcopy


class SudokoSolver:
    def __init__(self, board):
        self.board = board
        self.solved = False

    def next_row(self, row, col):
        if col < 8:
            return row
        else:
            return row + 1

    def next_col(self, col):
        if col < 8:
            return col + 1
        else:
            return 0

    def solve(self, i=0, j=0):
        if i >= 9:
            self.solved = True
            return
        if self.board[i][j] != '':
            yield from self.solve_next_cell(i, j)
            return
        for x in range(9):
            self.board[i][j] = str(x+1)
            yield self.board
            if self.check_row(i) and self.check_col(j) and self.check_square(i, j):
                yield from self.solve_next_cell(i, j)
                if self.solved:
                    return
            self.board[i][j] = ''
            yield self.board

    def solve_next_cell(self, i, j):
        new_i = self.next_row(row=i, col=j)
        new_j = self.next_col(col=j)
        yield from self.solve(new_i, new_j)

    def check_row(self, row):
        d = set()
        for col in range(len(self.board)):
            val = self.board[row][col].strip()
            if val == '':
                continue
            if val in d:
                return False
            d.add(val)
        return True

    def check_col(self, col):
        d = set()
        for row in range(len(self.board)):
            val = self.board[row][col].strip()
            if val == '':
                continue
            if val in d:
                return False
            d.add(val)
        return True

    def check_square(self, row, col):
        d = set()
        square_start_row = row - (row % 3)
        square_start_col = col - (col % 3)
        for i in range(3):
            for j in range(3):
                val = self.board[square_start_row+i][square_start_col+j].strip()
                if val == '':
                    continue
                if val in d:
                    return False
                d.add(val)
        return True