from pydantic import BaseModel

class user_log_in(BaseModel): 
    user_name: str = ''
    password: str = ''

class user_token(BaseModel):
    user_name:str 
    password:str 
    grant_type:str
    

class TokenRequest(BaseModel):
    user_name: str
    password: str

class UserCreate(BaseModel):
    user_name: str
    phone_number: int
    email: str
    password: str
    
