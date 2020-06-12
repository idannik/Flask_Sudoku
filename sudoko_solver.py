from board_options_manager import BoardOptionsManager


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
                val = self.board[square_start_row + i][square_start_col + j]
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
    def __init__(self, board, board_options_handler=None):
        super().__init__(board)
        self.options_handler = board_options_handler or BoardOptionsManager(self.board)
        self.options_handler.init_board_options(self.board)
        self.options_handler.update_board_options(self.board)

    def solve(self):
        while True:
            next_steps = self.options_handler.next_step()
            if not next_steps:
                return
            for (i, j), val in next_steps:
                self.options_handler.options[i][j] = set()
                self.board[i][j] = val
                yield self.board
                self.update_board_options_according_to_cell(i, j)

    def update_board_options_according_to_cell(self, row, col):
        val = self.board[row][col]
        return self.options_handler.update_board_options_according_to_cell(row, col, val)

    def print_options(self):
        self.options_handler.print_options()
