import os
import time
from flask_cors import CORS

from flask import Flask
from flask import render_template
from flask import request

from SodukoUtils import init_board_options
from data.sudopy import Sudoku
from sudoko_solver import SudokuSuggester
from flask import Flask

app = Flask(__name__)
CORS(app)

@app.route("/greeting")
def greeting():
    return {"greeting": "Hello from Flask!"}

if 'HEROKU' in os.environ:
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['DEBUG'] = os.environ['DEBUG']


@app.route('/')
@app.route('/index')
def index():
    return 'hi'


@app.route('/get_board/<int:board_id>', methods=['GET'])
def handle_connect(board_id):
    print('got load request')
    b = Sudoku(board_id).board
    return {'board': b, 'id': 0}


@app.route('/get_pencil_marks', methods=['GET', 'POST'])
def get_options():
    print('got load options')
    message = request.get_json()
    options = init_board_options(message['board'])
    return {'options': options}



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
