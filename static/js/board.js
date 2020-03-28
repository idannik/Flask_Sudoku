$(document).ready(function () {
    var socket = io();

    $('#solve-btn').click(function () {
        let board = []
        for (let i = 0; i < 9; i++) {
            let row = []
            for (let j = 0; j < 9; j++) {
                row[j] = document.querySelector(`#cell-input\\[0\\]\\[${i * 9 + j}\\]`).value
            }
            board[i] = row
        }
        socket.emit('solve', {board: board});
    })

    socket.on('update_board', function (message) {
        board = message['board']
        console.log(message)
        console.log('here')
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                document.querySelector(`#cell-input\\[0\\]\\[${i * 9 + j}\\]`).value = board[i][j]
            }
        }
    });

});