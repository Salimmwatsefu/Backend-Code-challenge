#  **FlASK SQLite3 Q&A APP**

This is a Flask app for creating and managing Q&A content stored in an SQLite3 database. The app allows users to register, login, post questions, answers the questions, and update/delete questions and answers.

## *Requirements*
-Python 3.6 or higher
-Flask
-Werkzeug
-SQLite3


## *Installation*
-Clone the repository to your local machine
-Ensure that the environment is active
-Install the required dependencies with pip install -r requirements.txt
-Create a new SQLite3 database by running the database.py script in the terminal with *python3 database.py*
-Run the app with *python3 app.py*


## Endpoints
### *GET /*
This endpoint returns a simple message to check if the app is running.

### *POST /auth/register*
This endpoint allows users to register with a username and password. The endpoint hashes the password and stores it in the database.

### *POST /auth/login*
This endpoint allows registered users to log in with their username and password. The endpoint creates a session for the user by storing the user's ID in a cookie.

### *GET /questions*
This endpoint returns a JSON object containing all the questions in the database.

### *POST /questions*
This endpoint allows authenticated users to post a new question. The endpoint checks if the user is authenticated and stores the question in the database.

### *GET /questions/<int:question_id>*
This endpoint returns a JSON object containing a specific question and all its answers.

### *DELETE /questions/<int:question_id>*
This endpoint allows authenticated users to delete a specific question and all its answers. The endpoint checks if the user is authenticated and is the author of the question.

### *POST /questions/<int:question_id>/answers*
This endpoint allows authenticated users to post an answer to a specific question. The endpoint checks if the user is authenticated and stores the answer in the database.

### *PUT /questions/<int:question_id>/answers/<int:answer_id>*
This endpoint allows authenticated users to update a specific answer. The endpoint checks if the user is authenticated and is the author of the answer.

### *DELETE /questions/<int:question_id>/answers/<int:answer_id>*
This endpoint allows authenticated users to delete a specific answer. The endpoint checks if the user is authenticated and is the author of the answer.








