from pydantic import BaseModel, Field


## Auth ##

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


## Todos ##

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=5, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


## Users ##

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)




