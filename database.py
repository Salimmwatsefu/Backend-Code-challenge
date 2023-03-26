import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)

cursor = conn.cursor()

cursor.execute(''' CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL UNIQUE,
password TEXT NOT NULL
)''')

cursor.execute(''' CREATE TABLE questions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
body TEXT NOT NULL,
writer_id INTEGER NOT NULL,
FOREIGN KEY (writer_id) REFERENCES users(id)
)''')

cursor.execute(''' CREATE TABLE answers(
id INTEGER PRIMARY KEY AUTOINCREMENT,
body TEXT NOT NULL,
question_id INTEGER NOT NULL,
writer_id INTEGER NOT NULL,
FOREIGN KEY (question_id) REFERENCES questions(id)
FOREIGN KEY (writer_id) REFERENCES users(id)
)''')

