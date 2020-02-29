import os

from flask import Flask
from flask import render_template, request, flash, redirect, url_for
from flask_socketio import SocketIO, emit

from data.sudopy import Sudoku

# data.config.from_object('local_config')

app = Flask(__name__)

socketio = SocketIO(app)


if 'HEROKU' in os.environ:
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['DEBUG'] = os.environ['DEBUG']


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', board=Sudoku().board)


@socketio.on('my_event')
def handle_my_custom_event(json):
    emit('my_response',
         {'new_board': Sudoku().board})

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('solve')
def handle_message(board):
    print('received message: ' + str(board))


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