from board_options_manager import BoardOptionsManager


def create_options(values: dict):
    board_options = [[set() for _0 in range(9)] for _1 in range(9)]
    for (row, col), val in values.items():
        board_options[row][col] = val
    return board_options


class TestBoardOptions:

    def test_simple_next_step(self):
        options = create_options({
            (0, 0): {1}
        })
        handler = BoardOptionsManager(options)
        assert handler.next_step() == {((0, 0), 1)}

    def test_naked_pair_row(self):
        options = create_options({
            (0, 0): {1, 2},
            (0, 1): {1, 2},
            (0, 2): {1, 2, 3}
        })
        handler = BoardOptionsManager(options)
        handler.update_board_options_according_to_cell(0, 0, 0)

        assert handler.options[0][2] == {3}

    def test_naked_pair_col(self):
        options = create_options({
            (0, 0): {1, 2},
            (1, 0): {1, 2},
            (2, 0): {1, 2, 3}
        })
        handler = BoardOptionsManager(options)
        handler.update_board_options_according_to_cell(0, 0, 0)

        assert handler.options[2][0] == {3}

    def test_naked_triple_row(self):
        options = create_options({
            (0, 0): {1, 2, 3},
            (0, 1): {1, 2, 3},
            (0, 2): {1, 2, 3},
            (0, 3): {1, 2, 3, 5}

        })
        handler = BoardOptionsManager(options)
        handler.update_board_options_according_to_cell(0, 0, 0)

        assert handler.options[0][3] == {5}

    def test_naked_quadruple_row(self):
        options = create_options({
            (0, 0): {1, 2, 3, 4},
            (0, 1): {1, 2, 3, 4},
            (0, 2): {1, 2, 3, 4},
            (0, 3): {1, 2, 3, 5},
            (0, 4): {1, 2, 3, 4}

        })
        handler = BoardOptionsManager(options)
        handler.update_board_options_according_to_cell(0, 0, 0)

        assert handler.options[0][3] == {5}

    def test_hidden_pair_row(self):
        options = create_options({
            (0, 0): {1, 2, 3},
            (0, 1): {1, 2, 3},
            (0, 2): {3, 4, 5}
        })
        handler = BoardOptionsManager(options)
        handler.update_board_options_according_to_cell(0, 0, 0)

        assert handler.options[0][0] == {1, 2}
        assert handler.options[0][1] == {1, 2}
