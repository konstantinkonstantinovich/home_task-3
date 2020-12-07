import os.path
import sqlite3
import json
from faker import Faker

fake = Faker(['en-US'])


DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'costumers.db')
DURA = os.path.join(os.path.dirname(__file__), 'tracks.db')


def generate_user(count=0):
    for _ in range(count):
        FirstName = fake.first_name()
        yield FirstName


def init_database():
    with sqlite3.connect(DEFAULT_PATH) as conn:
        with conn as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS costumers 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName text)"""
            )
            for user in generate_user(30):
                cursor.execute(
                    """INSERT INTO costumers(FirstName) VALUES (?)""",
                    (user,)
                )
    with sqlite3.connect(DURA) as conn:
        with conn as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS tracks 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist TEXT, 
                genre TEXT,
                title TEXT,
                sec INTEGER NO NULL DEFAULT  0)"""
            )
            with open('static/mus.json') as r:
                d = json.load(r)
                for i in range(len(d)):
                    t = d[i]['sec'].split(':')
                    sec = int(t[0]) * 60 + int(t[1])
                    cursor.execute(
                        """INSERT INTO tracks(artist, genre, title, sec) VALUES (?, ?, ?, ?)""",
                        (d[i]['artist'], d[i]['genre'].replace(' ', '_'), d[i]['title'].replace(' ', ''), sec)
                    )


def exec_query(query, *args):
    with sqlite3.connect(DEFAULT_PATH) as conn:
        with conn as cursor:
            qs = cursor.execute(query, args)
            results = qs.fetchall()
    return results


if __name__ == "__main__":
    init_database()
