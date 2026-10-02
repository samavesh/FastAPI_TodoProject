from fastapi import APIRouter, Request
from starlette import status
from starlette.responses import RedirectResponse
from ..models import Todos
from ..routers.auth import get_current_user
from ..routers.todos import db_dependency
from ..templates import templates

router = APIRouter(
    prefix="/todos",
    tags=["todos-pages"]
)

@router.get("/todo")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return redirect_to_login()
        user = await get_current_user(token)
        if user is None:
            return redirect_to_login()
        todos = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()
        return templates.TemplateResponse(request=request, name="todo.html", context={"todos": todos, "user": user})
    except:
        return redirect_to_login()


@router.get("/add-todo")
async def render_add_todo_page(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return redirect_to_login()
        user = await get_current_user(token)
        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse(request=request, name="add-todo.html", context={"user": user})
    except:
        return redirect_to_login()


@router.get("/edit-todo/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return redirect_to_login()
        user = await get_current_user(token)
        if user is None:
            return redirect_to_login()

        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        return templates.TemplateResponse(request=request, name="edit-todo.html", context={"todo": todo, "user": user})
    except:
        return redirect_to_login()



def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response