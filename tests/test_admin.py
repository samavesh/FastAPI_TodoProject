from .utils import *
from TodoApp.routers.admin import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todos")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'title': 'Learn to Code!',
        'description': 'Learn everyday!',
        'complete': False,
        'id': 1,
        'priority': 5,
        'owner_id': 1
    }]


def test_admin_delete_todo(test_todo):
    response = client.delete(f"/admin/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_admin_delete_todo_not_found(test_todo):
    response = client.delete(f"/admin/todo/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': 'Todo not found.'
    }


def test_admin_get_all_users_authenticated(test_user):
    response = client.get("/admin/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['username'] == 'tomhardy'
    assert response.json()[0]['email'] == 'tomhardy@gmail.com'
    assert response.json()[0]['first_name'] == 'Tom'
    assert response.json()[0]['last_name'] == 'Hardy'
    assert response.json()[0]['role'] == 'admin'
    assert response.json()[0]['phone_number'] == '9876543210'


def test_admin_delete_user(test_user):
    response = client.delete(f"/admin/user/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Users).filter(Users.id == 1).first()
    assert model is None


def test_admin_delete_user_not_found(test_user):
    response = client.delete(f"/admin/user/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': 'User not found.'
    }
