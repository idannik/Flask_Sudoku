document.addEventListener("DOMContentLoaded", function () {
    var socket = io();

    window.focus_cell = {
        index: -1,
        row: -1,
        col: -1
    };

    const query_soduko_cell = (id, square, cell) => {
        return document.querySelector(`#sudoku${id} > div:nth-child(${square}) > div:nth-child(${cell})`);
    }

    const get_cell_accroding_to_row_and_col = (row, col, id) => {
        const square = Math.floor(row / 3) * 3 + Math.floor(col / 3) + 1
        const cell = (row % 3) * 3 + col % 3 + 1
        return query_soduko_cell(id, square, cell)
    }

    const no_focus_on_cell = () => {
        return window.focus_cell.index == -1 && window.focus_cell.row == -1 && window.focus_cell.col == -1
    }

    const get_focus_cell = () => {
        return get_cell_accroding_to_row_and_col(window.focus_cell.row,
            window.focus_cell.col,
            window.focus_cell.index)
    };

    const unfocus_old_cell = () => {
        if (no_focus_on_cell()) {
            return
        }

        div = get_focus_cell()
        if (div) {
            div.style.backgroundColor = ""
        }
        focus_cell.index = -1
        focus_cell.row = -1
        focus_cell.col = -1
    };


    function set_div_pencil_mode(div, pencil_mode) {
        if (div.pencil_mode != pencil_mode) {
            div.textContent = ""
        }
        div.pencil_mode = pencil_mode;
        let color = 'moccasin'
        let fontSize = ''
        let fontWeight = ''
        if (div.pencil_mode) {
            color = 'paleturquoise'
            fontSize = '175%'
            fontWeight = 'bold'
        }
        div.style.backgroundColor = color
        div.style.fontSize = fontSize
        div.style.fontWeight = fontWeight

    }

    const init_cell_on_click = () => {
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                let div = get_cell_accroding_to_row_and_col(i, j, 0)
                if (div) {
                    div.onclick = (event) => {
                        if (!event.target.disabled) {
                            unfocus_old_cell()
                            window.focus_cell.index = 0;
                            window.focus_cell.row = i;
                            window.focus_cell.col = j;

                            set_div_pencil_mode(event.target, event.altKey);
                        }
                    }
                    div.onkeypress = (event) => {
                        let target = event.target
                        if (!target.disabled) {
                            if (event.key >= 1 && event.key <= 9) {
                                const key = event.key
                                if (target.pencil_mode) {
                                    const numbers = target.textContent.split(" ")
                                    const idx = numbers.findIndex(x => x === key)
                                    if (idx === -1) {
                                        numbers.push(key)
                                        numbers.sort()
                                    } else {
                                        numbers.splice(idx, 1)
                                    }
                                    target.textContent = numbers.join(" ")
                                } else {
                                    target.textContent = event.key
                                }
                            }
                        }
                    }

                }
            }
        }
    }
    init_cell_on_click()


    document.querySelector("#solve-btn").onclick = function () {
        let board = []
        for (let id = 0; id < 1; id++) {
            for (let i = 0; i < 9; i++) {
                let row = []
                for (let j = 0; j < 9; j++) {
                    let val = get_cell_accroding_to_row_and_col(i, j, id).textContent
                    if (val === '') {
                        row[j] = 0
                    } else {
                        row[j] = parseInt(val)
                    }

                }
                board[i] = row
            }
            socket.emit('solve', {board: board, id: id});
        }
    }


    socket.on('update_board', function (message) {
        const board = message['board']
        const id = message["id"]
        console.log(message)
        console.log('here2')
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                let div = get_cell_accroding_to_row_and_col(i, j, id)
                if (div) {
                    if (board[i][j] > 0) {
                        div.textContent = board[i][j]
                        div.disabled = true
                        div.style.backgroundColor = "lightgray"
                    } else {
                        div.textContent = ""
                        div.disabled = false
                    }
                    div.pencil_mode = false
                }

            }
        }
    });
});

