from pydantic import BaseModel

class UserLogIn(BaseModel): 
    userName: str = ''
    password: str = ''

class TokenRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    phoneNumber: int
    email: str
    password: str
    
