from flask import Flask, render_template
from flask_socketio import SocketIO

from player_utils import queue, player

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
sio = SocketIO(app, async_mode='threading')


@sio.on('connect')
def update_index():
    if player is None or player.props.status != 'Playing':
        return
    artist = player.get_artist()
    title = player.get_title()
    queue.put((artist, title))


@app.route('/')
def index():
    return render_template('index.html')


def run_server():
    sio.run(app)
