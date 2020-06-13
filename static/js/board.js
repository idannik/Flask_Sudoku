$(document).ready(function () {
    var socket = io();
    console.log('here')


    function query_soduko_cell(id, square, cell) {
        return document.querySelector(`#sudoku${id} > div:nth-child(${square}) > div:nth-child(${cell})`);
    }

    const get_cell_accroding_to_row_and_col = (row, col, id) => {
        const square = Math.floor(row / 3) * 3 + Math.floor(col / 3) + 1
        const cell = (row % 3 )* 3 + col % 3 + 1
        return query_soduko_cell(id, square, cell)
    }

    $('#solve-btn').click(function () {
        let board = []
        for (let id=0; id<1; id++) {
            for (let i = 0; i < 9; i++) {
                let row = []
                for (let j = 0; j < 9; j++) {
                    let val = get_cell_accroding_to_row_and_col(i, j, id).textContent
                    if (val=='') {
                        row[j] = 0
                    } else {
                        row[j] = parseInt(val)
                    }

                }
                board[i] = row
            }
            socket.emit('solve', {board: board, id:id});
        }
    })



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
                    } else {
                        div.textContent = ""
                        div.disabled = false
                    }
                }

            }
        }
    });

});
