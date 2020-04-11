$(document).ready(function () {
    var socket = io();
    console.log('here')



    const get_cell_accroding_to_row_and_col = (row, col, id) => {
        const square = Math.floor(row / 3) * 3 + Math.floor(col / 3) + 1
        const cell = (row % 3 )* 3 + col % 3 + 1
        return document.querySelector(`#sudoku${id} > div:nth-child(${square}) > input:nth-child(${cell})`)
    }

    $('#solve-btn').click(function () {
        let board = []
        for (let id=0; id<2; id++) {
            for (let i = 0; i < 9; i++) {
                let row = []
                for (let j = 0; j < 9; j++) {
                    row[j] = get_cell_accroding_to_row_and_col(i, j, id).value
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
                if (board[i][j]>0) {
                    div.value = board[i][j]
                    div.disabled = true
                } else {
                    div.value = ''
                    div.disabled = false
                }

            }
        }
    });

});
