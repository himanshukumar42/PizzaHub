from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class PizzaSize(str, Enum):
    small = "Small"
    medium = "Medium"
    large = "Large"
    x_large = "Extra-Large"


class OrderStatus(str, Enum):
    pending = "Pending"
    in_transit = "In-transit"
    delivered = "Delivered"


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
    order_status: Optional[OrderStatus] = "Pending"
    pizza_size: Optional[PizzaSize] = "Small"

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "pizza_size": "Small",
                "quantity": 1,
            }
        }


class OrderStatusModel(BaseModel):
    order_status: Optional[OrderStatus] = "Pending"

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "order_status": "Pending",
            }
        }
