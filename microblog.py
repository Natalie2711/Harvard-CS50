
import datetime
import os
 
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

# some lines omitted here

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route('/time')
def time():
    now = datetime.datetime.now()
    new_year = now.month == 1 and now.day == 1
    return render_template("year.html", new_year = new_year )

@app.route('/loop')
def loop():
    names = ['alice', 'claire','chan']
    return render_template("loop.html", names = names)


votes = {"yes": 0, "no": 0, "maybe": 0}

@app.route("/")
def index():
    return render_template("index.html", votes=votes)


@socketio.on("submit vote")
def vote(data):
    selection = data["selection"]
    votes[selection] += 1
    emit("vote totals", votes, broadcast=True)


@app.route("/hello")
def hello():
    return render_template('hello.html')


@app.route('/welcome')
def counter():
    return render_template('counter.html')