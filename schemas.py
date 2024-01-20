from pydantic import BaseModel, EmailStr
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: EmailStr
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "Johndoe@123",
                "is_staff": False,
                "is_active": True,
            }
        }
