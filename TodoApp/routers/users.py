from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path, HTTPException
from starlette import status
from ..models import Todos, Users
from ..database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix="/user",
    tags=["user"]
)                           # Create an APIRouter instance for user-related routes with a prefix of "/user" and a tag of "user" for documentation purposes.

def get_db():                     # Dependency function to get a database session. It creates a new session using SessionLocal, yields it for use in the route handlers, and ensures that the session is closed after use.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]                # Dependency that provides a database session to route handlers. It uses the get_db function to create and manage the session lifecycle.
user_dependency = Annotated[dict, Depends(get_current_user)]                # Dependency that provides the current authenticated user to route handlers. It uses the get_current_user function to retrieve the user information based on the authentication token provided in the request.
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')                  # Create a CryptContext instance for password hashing and verification using the bcrypt algorithm. The deprecated='auto' option allows automatic handling of deprecated hashing schemes.

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error on password change')

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)

    db.add(user_model)
    db.commit()


@router.put('/phonenumber/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.phone_number = phone_number

    db.add(user_model)
    db.commit()



















