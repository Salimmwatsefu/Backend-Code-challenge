import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_register(client):
    response = client.post('/auth/register', json={"username": "cristiano", "password": "testpassword"})
    assert response.status_code == 200
    assert b'User registered successfully' in response.data


def test_login(client):
    response = client.post('/auth/login', json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert b'User logged in successfully' in response.data


def test_questions(client):
    response = client.get('/questions')
    assert response.status_code == 200
    assert b'questions' in response.data


def test_get_question(client):
    response = client.get('/questions/1')
    assert response.status_code == 200
    assert b'question' in response.data
    assert b'answers' in response.data

