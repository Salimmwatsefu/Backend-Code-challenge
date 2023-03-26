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
    

#FETCH ALL QUESTIONS

@app.route('/questions', methods=['GET'])
def questions():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()

    return jsonify({"questions": questions})




#POST A QUESTION

@app.route('/questions', methods=['POST'])
def post_question():
    # Check if the user is authenticated
    user_id = request.cookies.get('user_id')
    if not user_id:
        return jsonify({"error": "Authentication required."})
    
    data = request.get_json()
    body = data.get('body')

    cursor = conn.cursor()
    cursor.execute("INSERT INTO questions (body, writer_id) VALUES (?, ?)", (body, user_id))
    conn.commit()

    return jsonify({"message": "Question posted successfully."})




#FETCH A SPECIFIC QUESTION AND ALL IT'S ANSWERS

@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id=?", (question_id,))
    question = cursor.fetchone()
    cursor.execute("SELECT * FROM answers WHERE question_id=?", (question_id,))
    answers = cursor.fetchall()

    return jsonify({"question": question, "answers": answers})



