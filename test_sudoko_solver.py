import pytest

from sudoko_solver import SudokoSmartSolver


class TestSudokoSmartSolver:
    def test_init_board_options(self):
        board = [
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 1, 3, 4, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 9, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0],
            [7, 0, 2, 0, 0, 0, 0, 0, 0],
            [9, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        solver = SudokoSmartSolver(board)
        assert solver.options_handler.options[2][4] == {5, 6, 7, 8, 9}
        assert solver.options_handler.options[0][0] == {8}
        assert solver.options_handler.options[3][2] == {6, 7, 8}

    def test_next_board_options(self):
        board = [
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 1, 3, 4, 0, 0, 0, 0, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 0],
            [5, 0, 9, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0],
            [7, 0, 2, 0, 0, 0, 0, 0, 0],
            [9, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        solver = SudokoSmartSolver(board)
        assert ((0,0), 8) in solver.options_handler.next_step()
