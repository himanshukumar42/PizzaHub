from pydantic import BaseModel, EmailStr
from typing import Optional, Any


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


class SignUpModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr
    password: str
    is_staff: Optional[bool] | None = False
    is_active: Optional[bool] | None = True

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "Johndoe@123",
                "is_staff": False,
                "is_active": True,
            }
        }


class LoginModel(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "Johndoe@123",
            }
        }
