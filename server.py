from flask import Flask, render_template
from flask_socketio import SocketIO

async_mode = 'threading'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
sio = SocketIO(app, async_mode=async_mode)


@app.route('/')
def index():
    return render_template('index.html', async_mode=sio.async_mode)
