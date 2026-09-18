from fastapi.testclient import TestClient
from TodoApp.main import app
from fastapi import status

client = TestClient(app)              # This line creates an instance of TestClient, which is a testing utility provided by FastAPI. It allows you to simulate HTTP requests to your FastAPI application without running a live server. The app parameter is passed to the TestClient constructor, which is the FastAPI application instance defined in the main.py file. This enables you to test the endpoints and functionality of your FastAPI application in a controlled environment.


def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}

