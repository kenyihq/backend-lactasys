from pydantic import BaseModel

class LoginRequest(BaseModel):
    documento: str
    password: str