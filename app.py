from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

conn = sqlite3.connect("database.db",check_same_thread=False)

##Endpoints##

#testing
@app.route('/')
def home():
    return ("Hello there")

#Register a user

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    hashed_password = generate_password_hash(password)

    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()

    return jsonify({"message": "User registered successfully"})


#Log a user in

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    # Check if the user exists and the password is correct
    if user and check_password_hash(user[1], password):
        # Create a session for the user by storing the user's ID in a cookie
        response = jsonify({"message": "User logged in successfully."})
        response.set_cookie('user_id', str(user[0]))
        return response
    else:
        return jsonify({"error": "Invalid username or password."})
