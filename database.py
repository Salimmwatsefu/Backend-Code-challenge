import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)

cursor = conn.cursor()

cursor.execute(''' CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL UNIQUE,
password TEXT NOT NULL
)''')