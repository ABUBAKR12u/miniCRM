from pydantic import BaseModel

class AddLogin(BaseModel):
    username: str
    password: str

class UpdateLogin(AddLogin):
    pass

class ResponseLogin(BaseModel):
    id: int
    username: str
    password: str
    role: str

class RefreshToken(BaseModel):
    access_token: str