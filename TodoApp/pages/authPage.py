from fastapi import APIRouter, Request
from ..templates import templates


router = APIRouter(
    prefix="/auth",
    tags=["auth-pages"]
)

@router.get("/login")
def render_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@router.get("/register")
def render_register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")
