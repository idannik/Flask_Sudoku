import os
import time

from flask import Flask
from flask import render_template
from flask_socketio import SocketIO, emit

from data.sudopy import Sudoku
from sudoko_solver import SudokoSmartSolver

# data.config.from_object('local_config')

app = Flask(__name__)

socketio = SocketIO(app)

if 'HEROKU' in os.environ:
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['DEBUG'] = os.environ['DEBUG']


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@socketio.on('board_load')
def handle_connect(json):
    print('got load request')
    b = Sudoku(json['board_id']).board
    emit('update_board', {'board': b, 'id': 0})


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('solve')
def handle_message(message):
    solver = SudokoSmartSolver(message['board'])
    solver.print_options()
    print(solver.stringify())
    for s in solver.solve():
        emit('update_board', {'board': s.board,
                              'options': list(s.get_options_list()),
                              'id': message['id']})
        time.sleep(0.05)
    emit('update_board', {'board': solver.board,
                          'options': list(solver.get_options_list()),
                          'id': message['id']})
    print('DONE')


@app.route('/solution', methods=['POST'])
def solution():
    print('hi')


def clean_puzzle(puzzle):
    """
    converts input from request.form to a string format readable by Sudoku
    """
    output = ''
    for val in puzzle.values():
        if val == '':
            output += '.'
        elif int(val) in range(1, 10):
            output += val
    return output
