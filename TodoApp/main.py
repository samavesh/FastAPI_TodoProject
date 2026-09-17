from fastapi import FastAPI, Request, status
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
# from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()                  # Create the FastAPI instance

# models.Base.metadata.create_all(bind=engine)            # Create the database tables based on the models defined in models.py
Base.metadata.create_all(bind=engine)            # Create the database tables based on the models defined in models.py

# templates = Jinja2Templates(directory='ToDoApp/templates')           # Create a Jinja2Templates instance to render HTML templates. The directory parameter specifies the location of the templates folder, which contains the HTML files used for rendering views in the application.

app.mount('/static', StaticFiles(directory='ToDoApp/static'), name='static')

@app.get("/")                      # Define a route for the root URL ("/") of the application. This route will handle GET requests and render the "home.html" template when accessed. The request parameter is of type Request, which allows access to the incoming HTTP request data.
def test(request: Request):
    # return templates.TemplateResponse(request=request, name="home.html")
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


@app.get("/healthy")
def health_check():
    return {"status": "ok"}


app.include_router(auth.router)            
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)




