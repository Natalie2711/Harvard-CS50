
import datetime
import os

import requests
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
    return render_template("currency.html")


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

@app.route('/convert', methods = ['POST'])
def convert():
    # Query for currency exchange rate:
    currency = request.form.get('currency')
    res = requests.get('http://api.fixer.io/latest', params= {
        "base":"USD", "symbol":currency})
    # Check if the request is successful:
    if res.status_code != 200:
        return jsonify({'success':False})
     # Make sure currency is in response

    data = res.json()
    if currency not in data['rates']:
        return jsonify({'success':False})
    
