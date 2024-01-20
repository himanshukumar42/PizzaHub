from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, index=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    orders = relationship("Order", back_populates="user")

    def __repr__(self) -> str:
        return f"<User: {self.username}>"

    def __str__(self) -> str:
        return f"User: {self.username}"


class Order(Base):
    ORDER_STATUS = (
        ("PENDING", "pending"),
        ("IN-Transit", "in-transit"),
        ("DELIVERED", "delivered"),
    )

    PIZZA_SIZE = (
        ("SMALL", "small"),
        ("MEDIUM", "medium"),
        ("LARGE", "large"),
        ("EXTRA-LARGE", "extra-large"),
    )
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default="PENDING")
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZE), default="SMALL")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")

    def __repr__(self) -> str:
        return f"<Order: {self.id}>"

    def __str__(self) -> str:
        return f"Order: {self.id}"
