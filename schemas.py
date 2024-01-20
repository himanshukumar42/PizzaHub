from pydantic import BaseModel, EmailStr
from typing import Optional


class Settings(BaseModel):
    authjwt_secret_key: str = "d4a87b4d993046d7329c6af4a091ea249575deae4dc4d6b3692a08de80537bda"


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: EmailStr
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        from_attributes = True
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
