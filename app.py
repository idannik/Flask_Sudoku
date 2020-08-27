import os
from copy import deepcopy

from flask import Flask, make_response
from flask import session
from flask_cors import CORS
from flask_session import Session

from SodukoUtils import init_board_options, find_next_move
from data.sudopy import Sudoku

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.secret_key = b'abjdslgjl'
app.config.from_object(__name__)
CORS(app, supports_credentials=True)
Session(app)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',
)



@app.route("/greeting")
def greeting():
    return {"greeting": "Hello from Flask!"}



@app.route('/')
@app.route('/index')
def index():
    return 'hi'


@app.route('/get_board/<int:board_id>', methods=['GET'])
def handle_connect(board_id):
    print('got load request')
    b = Sudoku(board_id).board
    print(f'old board data = ' + str(session.get('board')))
    print(f'old board a = ' + str(session.get('a')))

    session['board'] = b

    session['options'] = [[] * 9 for _ in range(9)]
    return {'board': b, 'id': 0}


def jsonify_options(options):
    res = deepcopy(options)
    for i in range(9):
        for j in range(9):
            res[i][j] = list(res[i][j])

    return res


@app.route('/get_pencil_marks', methods=['GET'])
def get_options():
    print('got load options')
    options = init_board_options(session['board'])
    session['options'] = options
    options_with_list_instead_of_sets = [[list(options[i][j]) for j in range(9)]for i in range(9)]
    return {'options': options_with_list_instead_of_sets}


@app.route('/next_step', methods=['GET'])
def get_next_step():
    print('got load options')
    return find_next_move()


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
