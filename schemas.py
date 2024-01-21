from pydantic import BaseModel, EmailStr
from typing import Optional, Any


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_access_token_expires: int = 300
    authjwt_refresh_token_expires: int = 300
    authjwt_algorithm: str = "HS256"


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


class OrderModel(BaseModel):
    id: Optional[int] = None
    quantity: int
    order_status: Optional[str] = "PENDING"
    pizza_size: Optional[str] = "SMALL"

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "quantity": 1,
                "pizza_size": "SMALL",
            }
        }
