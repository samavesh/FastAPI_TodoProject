from fastapi import FastAPI, Request, status
from .models import Users, Todos
from .database import Base, engine
from .routers import auth, todos, admin, users
from .pages import authPage, todosPage
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()                  # Create the FastAPI instance

# models.Base.metadata.create_all(bind=engine)            # Create the database tables based on the models defined in models.py
Base.metadata.create_all(bind=engine)            # Create the database tables based on the models defined in models.py

app.mount('/static', StaticFiles(directory='TodoApp/static'), name='static')          # Mount the static files directory to serve static assets (e.g., CSS, JavaScript, images) from the specified directory. The '/static' URL path will be used to access these static files in the application.

@app.get("/")                      # Define a route for the root URL ("/") of the application. This route will handle GET requests and render the "home.html" template when accessed. The request parameter is of type Request, which allows access to the incoming HTTP request data.
def test(request: Request):
    # return templates.TemplateResponse(request=request, name="home.html")
    return RedirectResponse(url="/todos/todo", status_code=status.HTTP_302_FOUND)


@app.get("/healthy")
def health_check():
    return {"status": "ok"}

# API routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

# HTML page routers
app.include_router(authPage.router)
app.include_router(todosPage.router)