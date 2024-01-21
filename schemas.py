from pydantic import BaseModel, EmailStr
from typing import Optional, Any


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool] | None = False
    is_active: Optional[bool] | None = True

    class Config:
        from_attributes = True


class LoginModel(BaseModel):
    username: str
    password: str
