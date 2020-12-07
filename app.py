import os
import sqlite3

from flask import Flask, render_template

from database import exec_query

app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(__file__), 'costumers.db')
DATABASE2 = os.path.join(os.path.dirname(__file__), 'tracks.db')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/first_task')
def index():
    users = list()
    with sqlite3.connect(DATABASE) as conn:
        with conn as cursor:
            for row in cursor.execute("SELECT COUNT(DISTINCT FirstName) FROM costumers"):
                users.append(row[0])
    return render_template("index.html", users=users)


@app.route('/second_task')
def second_task():
    u = list()
    with sqlite3.connect(DATABASE2) as conn:
        with conn as cursor:
            for row in cursor.execute("SELECT COUNT(DISTINCT title) FROM tracks"):
                u.append(row[0])
    return render_template("second.html", u=u)


@app.route('/third_task')
@app.route('/third_task/<genre>')
def third_task(genre):
    if genre == '':
        return "You haven't entered a genre"
    g = genre
    p = list()
    with sqlite3.connect(DATABASE2) as conn:
        with conn as cursor:
            for row in cursor.execute("SELECT COUNT(title) FROM tracks WHERE genre = (?)", (g,)):
                p.append(row[0])
    return render_template("third.html", p=p)


@app.route('/forth_task')
def forth_task():
    us = dict()
    with sqlite3.connect(DATABASE2) as conn:
        with conn as cursor:
            for row, col in cursor.execute("SELECT DISTINCT title, sec FROM tracks"):
                us[row] = col
    return render_template("forth.html", us=us)


@app.route('/fifth_task')
def fifth_task():
    with sqlite3.connect(DATABASE2) as conn:
        with conn as cursor:
            avg = cursor.execute("SELECT AVG(sec) FROM tracks").fetchone()[0]
            sum_of = cursor.execute("SELECT SUM(sec) FROM tracks").fetchone()[0]
    return render_template("fifth.html", avg=avg, sum_of=sum_of)


