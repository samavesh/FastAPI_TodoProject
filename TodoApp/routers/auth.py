from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from ..database import SessionLocal
from ..models import Users
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# Secret Key & Algorithm work together to create a secure token that can be used for authentication and authorization purposes. The SECRET_KEY is a random string that is used to sign the token, while the ALGORITHM specifies the hashing algorithm used to create the signature. Together, they ensure that the token cannot be tampered with or forged, and that it can be verified by the server when it is received in subsequent requests.
# SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY = '680e779350d3fb81d8f919db33e26f3a55c0864e8b7a3aef175ffb5532fa0472'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')               # This line creates an instance of OAuth2PasswordBearer, which is a class provided by FastAPI to handle OAuth2 authentication using bearer tokens. The tokenUrl parameter specifies the URL endpoint where clients can obtain the access token. In this case, it is set to 'auth/token', indicating that clients should send their credentials to this endpoint to receive a token for authentication in subsequent requests.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

templates = Jinja2Templates(directory='TodoApp/templates')           # Create a Jinja2Templates instance to render HTML templates. The directory parameter specifies the location of the templates folder, which contains the HTML files used for rendering views in the application.

### Pages ###

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")


@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")


### Endpoints ###

class CreateUserRequest(BaseModel):           # This class defines the structure of the request body for creating a new user. It inherits from Pydantic's BaseModel, which provides data validation and serialization capabilities. The class contains several attributes that represent the required fields for creating a user, including username, email, first_name, last_name, password, and role. Each attribute is defined with its corresponding data type (str) to ensure that the incoming request data adheres to the expected format.
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

class Token(BaseModel):              # This class defines the structure of the response body for the access token returned after successful authentication. It inherits from Pydantic's BaseModel and contains two attributes: access_token and token_type. The access_token attribute is a string that represents the generated JWT access token, while the token_type attribute is also a string that indicates the type of token (e.g., "bearer"). This class is used to serialize the response data when returning the access token to the client after successful login.
    access_token: str
    token_type: str

def authenticate_user(username: str, password: str, db):               # This function is responsible for authenticating a user based on their username and password. It takes three parameters: username (the username provided by the user), password (the password provided by the user), and db (the database session used to query the Users table). The function first queries the database to find a user with the given username. If no user is found, it returns False. If a user is found, it verifies the provided password against the hashed password stored in the database using bcrypt. If the password does not match, it returns False. If both the username and password are valid, it returns the user object.
    # user = Users.query.filter_by(username=username).first()
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):                # This function is responsible for creating a JSON Web Token (JWT) access token for a user. It takes four parameters: username (the username of the authenticated user), user_id (the unique identifier of the user), role (the role of the user), and expires_delta (a timedelta object representing the expiration time of the token). The function creates a dictionary called encode that contains the user's username, ID, and role. It then calculates the expiration time by adding the expires_delta to the current UTC time. The expiration time is added to the encode dictionary under the key 'exp'. Finally, the function encodes the dictionary into a JWT using the SECRET_KEY and ALGORITHM specified earlier, and returns the encoded token.

    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):                  # This function is responsible for retrieving the current authenticated user based on the provided JWT access token. It takes a single parameter token, which is obtained from the request's Authorization header using the OAuth2PasswordBearer dependency. The function attempts to decode the token using the SECRET_KEY and ALGORITHM specified earlier. If the decoding is successful, it extracts the username, user ID, and role from the decoded payload. If any of these values are missing or if the token is invalid, it raises an HTTPException with a 401 Unauthorized status code. If the token is valid, it returns a dictionary containing the username, user ID, and role of the authenticated user.
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        phone_number=create_user_request.phone_number,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}


'''
                    ┌─────────────────────┐
                    │   User visits site  │
                    └──────────┬──────────┘
                               │
                     ┌─────────▼─────────┐
                     │ Register / Login  │
                     └─────────┬─────────┘
                               │
             ┌─────────────────┴─────────────────┐
             │                                   │
       NEW USER                              EXISTING USER
             │                                   │
             ▼                                   ▼
    /auth/register-page                    /auth/login-page
             │                                   │
             ▼                                   ▼
       register.html                         login.html
             │                                   │
             ▼                                   ▼
       POST /auth/                         POST /auth/token
             │                                   │
             ▼                                   ▼
       create_user()                    authenticate_user()
             │                                   │
             ▼                                   ▼
       Hash password                    Verify password
             │                                   │
             ▼                                   ▼
       Save Users row                  create_access_token()
                                             │
                                             ▼
                                          JWT token
                                             │
                                             ▼
                                      Client stores token
                                             │
                                             ▼
                              Subsequent protected request
                                             │
                                             ▼
                                      oauth2_bearer
                                             │
                                             ▼
                                      get_current_user()
                                             │
                                             ▼
                                    JWT decoded/validated
                                             │
                                             ▼
                                   Current user identified
                                             │
                                             ▼
                              Authorization / role checking
'''