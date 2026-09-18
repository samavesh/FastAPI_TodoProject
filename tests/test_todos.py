from TodoApp.routers.todos import get_db, get_current_user
from fastapi import status
from .utils import *

# Overriding needs to be from the relative path of what is being tested. In this case, the get_db function is defined in the routers.todos module, so we use app.dependency_overrides[get_db] to override it with the override_get_db function. It is because the get_db function is imported into the routers.todos module, and we want to ensure that when the application requests a database session during testing, it will receive a session connected to the test database instead of the production database.
app.dependency_overrides[get_db] = override_get_db               # Override the get_db dependency in the FastAPI application to use the override_get_db function. This ensures that when the application requests a database session during testing, it will receive a session connected to the test database instead of the production database.
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_todos_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id': 1,
        'title': 'Learn to Code!',
        'description': 'Learn everyday!',
        'priority': 5,
        'complete': False,
        'owner_id': 1
    }]


def test_read_todo_authenticated(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        'title': 'Learn to Code!',
        'description': 'Learn everyday!',
        'priority': 5,
        'complete': False,
        'owner_id': 1
    }


def test_read_todo_authenticated_not_found(test_todo):
    response = client.get("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': 'Todo not found.'
    }


def test_create_todo(test_todo):
    request_data = {
        'title': 'Learn FastAPI!',
        'description': 'It is awesome!',
        'priority': 4,
        'complete': False
    }

    response = client.post('/todos/todo/', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data['title']
    assert model.description == request_data['description']
    assert model.priority == request_data['priority']
    assert model.complete == request_data['complete']


def test_update_todo(test_todo):
    request_data = {
        'title': 'New title: Learn FastAPI!',
        'description': 'It is awesome and simple!',
        'priority': 5,
        'complete': False
    }

    response = client.put('/todos/todo/1', json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data['title']
    assert model.description == request_data['description']
    assert model.priority == request_data['priority']
    assert model.complete == request_data['complete']


def test_update_todo_not_found(test_todo):
    request_data = {
        'title': 'New title: Learn FastAPI!',
        'description': 'It is awesome and simple!',
        'priority': 5,
        'complete': False
    }

    response = client.put('/todos/todo/999', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': 'Todo not found.'
    }


def test_delete_todo(test_todo):
    response = client.delete('/todos/todo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found(test_todo):
    response = client.delete('/todos/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': 'Todo not found.'
    }




