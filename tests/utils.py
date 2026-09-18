from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from TodoApp.database import Base
from TodoApp.main import app
from fastapi.testclient import TestClient
import pytest
from TodoApp.models import Todos, Users
from TodoApp.routers.auth import bcrypt_context


SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)           # Create a database engine for the test database using SQLite. The connect_args={"check_same_thread": False} option allows multiple threads to access the database simultaneously, and the poolclass=StaticPool option ensures that the same connection is used for all requests during testing.

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)              # Create a session factory for the test database. This factory will be used to create new database sessions for each test case, ensuring that the tests are isolated and do not interfere with each other.

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'tomhardy', 'id': 1, 'user_role': 'admin'}

client = TestClient(app)

@pytest.fixture                   # This decorator marks the test_todo function as a fixture in pytest. Fixtures are used to set up and tear down resources needed for tests. In this case, the fixture sets up a test database entry for a todo item before the test runs and cleans it up afterward.
def test_todo():
    todo = Todos(
        title='Learn to Code!',
        description='Learn everyday!',
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo                # The yield statement allows the test function to run after the setup code has executed. It provides the test function with access to the todo object. After the test function completes, the code following the yield statement will execute, allowing for cleanup of resources.
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        email='tomhardy@gmail.com',
        username='tomhardy',
        first_name='Tom',
        last_name='Hardy',
        hashed_password=bcrypt_context.hash("testpassword"),
        is_active=True,
        role='admin',
        phone_number='9876543210'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()










