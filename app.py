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




#FETCH A SPECIFIC QUESTION AND ALL ITS ANSWERS

@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id=?", (question_id,))
    question = cursor.fetchone()
    cursor.execute("SELECT * FROM answers WHERE question_id=?", (question_id,))
    answers = cursor.fetchall()

    return jsonify({"question": question, "answers": answers})



#DELETE A QUESTION

@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_questions(question_id):
    #check if user is authenticated and is the question's writer
    user_id = request.cookies.get('user_id')
    cursor = conn.cursor()
    cursor.execute("SELECT writer_id FROM questions WHERE id=?", (question_id,))
    question_writer_id = cursor.fetchone()[0]
    if not user_id or int(user_id) != question_writer_id:
        return jsonify({"error": "Authentication required or not authorized."})
    
     #delete the question and its answers
    cursor.execute("DELETE FROM answers WHERE question_id=?", (question_id,))
    cursor.execute("DELETE FROM questions WHERE id=?", (question_id,))
    conn.commit()

    return jsonify({"message": "Question has been deleted."})


#POST AN ANSWER TO A QUESTION

@app.route('/questions/<int:question_id>/answers', methods=['POST'])
def post_answer(question_id):
    # Check if the user is authenticated
    user_id = request.cookies.get('user_id')
    if not user_id:
        return jsonify({"error": "Authentication required."})

    data = request.get_json()
    body = data.get('body')

    cursor = conn.cursor()
    cursor.execute("INSERT INTO answers (body, question_id, writer_id) VALUES (?, ?, ?)", (body, question_id, user_id))
    conn.commit()

    return jsonify({"message": "Answer has been posted successfully."})

#UPDATING AN ANSWER

@app.route('/questions/<int:question_id>/answers/<int:answer_id>', methods=['PUT'])
def update_answer(question_id, answer_id):
    # Check if the user is authenticated and is the author of the answer
    user_id = request.cookies.get('user_id')
    cursor = conn.cursor()
    cursor.execute("SELECT writer_id FROM answers WHERE id=?", (answer_id,))
    answer_writer_id = cursor.fetchone()[0]
    if not user_id or int(user_id) != answer_writer_id:
        return jsonify({"error": "Authentication required or not authorized."})

    data = request.get_json()
    body = data.get('body')

    cursor.execute("UPDATE answers SET body=? WHERE id=?", (body, answer_id))
    conn.commit()

    return jsonify({"message": "Answer updated successfully."})

#DELETING AN ANSWER

@app.route('/questions/<int:question_id>/answers/<int:answer_id>', methods=['DELETE'])
def delete_answer(question_id, answer_id):
    
    # Check if the user is authenticated and is the author of the answer
    user_id = request.cookies.get('user_id')
    cursor = conn.cursor()
    cursor.execute("SELECT writer_id FROM answers WHERE id=?", (answer_id,))
    answer_writer_id = cursor.fetchone()[0]
    if not user_id or int(user_id) != answer_writer_id:
        return jsonify({"error": "Authentication required or not authorized."})

    cursor.execute("DELETE FROM answers WHERE id=?", (answer_id,))
    conn.commit()

    return jsonify({"message": "Answer deleted successfully."})

if __name__ == '__main__':
    app.run(debug=True)




