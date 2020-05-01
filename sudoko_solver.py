from collections import Counter
from copy import deepcopy

class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.solved = False

    def stringify(self):
        return ''.join([str(self.board[i][j]) for i in range(9) for j in range(9)]).replace('0', '.')

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

    def solve_next_cell(self, i, j):
        new_i = self.next_row(row=i, col=j)
        new_j = self.next_col(col=j)
        yield from self.solve(new_i, new_j)

    def check_row(self, row):
        d = set()
        for col in range(9):
            val = self.board[row][col]
            if val == 0:
                continue
            if val in d:
                return False
            d.add(val)
        return True

    def check_col(self, col):
        d = set()
        for row in range(9):
            val = self.board[row][col]
            if val == 0:
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
                val = self.board[square_start_row+i][square_start_col+j]
                if val == 0:
                    continue
                if val in d:
                    return False
                d.add(val)
        return True

    def check_cell(self, row, col):
        return self.check_row(row) and self.check_col(col) and self.check_square(row, col)


class SudokoBacktrackSolver(SudokuSolver):
    def __init__(self, board):
        super().__init__(board)

    def solve(self, i=0, j=0):
        if i >= 9:
            self.solved = True
            return
        if self.board[i][j] != 0:
            yield from self.solve_next_cell(i, j)
            return
        for x in range(9):
            self.board[i][j] = x + 1
            yield self.board
            if self.check_cell(i, j):
                yield from self.solve_next_cell(i, j)
                if self.solved:
                    return
            self.board[i][j] = 0
            yield self.board



class SudokoSmartSolver(SudokuSolver):
    def __init__(self, board):
        super().__init__(board)
        self.board_options = []
        self.init_board_options()
        self.update_board_options()

    def init_board_options(self):
        for i in range(9):
            row = []
            for j in range(9):
                val = set()
                if self.board[i][j] == 0:
                    val = set((1, 2, 3, 4, 5, 6, 7, 8, 9))
                row.append(val)
            self.board_options.append(row)

    def update_board_options(self):
        for i in range(9):
            for j in range(9):
                self.update_board_options_according_to_cell(i, j)

    def update_board_options_according_to_cell(self, row, col):
        val = self.board[row][col]
        if val == 0:
            return
        for i in range(9):
            self.board_options[i][col].discard(val)
            self.board_options[row][i].discard(val)
        square_start_row = row - (row % 3)
        square_start_col = col - (col % 3)
        for i in range(3):
            for j in range(3):
                self.board_options[square_start_row + i][square_start_col + j].discard(val)

    def next_step(self):
        res = set()
        for i in range(9):
            for j in range(9):
                if len(self.board_options[i][j]) == 1:
                    value = next(iter(self.board_options[i][j]))
                    res.add(((i, j), value))
                for value in self.board_options[i][j]:
                    if self.only_value(i, j, value):
                        res.add(((i, j), value))
        return res

    def only_value_in_row(self, row, value):
        return len([k for k in range(9) if value in self.board_options[row][k]]) == 1

    def only_value_in_col(self, col, value):
        return len([k for k in range(9) if value in self.board_options[k][col]]) == 1

    def only_value_in_square(self, row, col, value):
        square_start_row = row - (row % 3)
        square_start_col = col - (col % 3)
        return len([(k,p) for p in range(3) for k in range(3) if value in self.board_options[square_start_row+p][square_start_col+k]]) == 1

    def only_value(self, row, col, value):
        return self.only_value_in_row(row, value) or \
               self.only_value_in_col(col, value) or \
               self.only_value_in_square(row, col, value)

    def solve(self):

        next_steps = self.next_step()
        while next_steps:
            for (i, j), val in next_steps:
                self.board_options[i][j] = set()
                self.board[i][j] = val
                yield self.board
                self.update_board_options_according_to_cell(i, j)
            next_steps = self.next_step()





