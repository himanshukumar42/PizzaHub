from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, Text, Enum
from sqlalchemy.orm import relationship
from schemas import PizzaSize, OrderStatus
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

    def __repr__(self):
        return f"<User: {self.username}>"


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(Enum(OrderStatus), default="pending")
    pizza_size = Column(Enum(PizzaSize), default="small")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")

    def __repr__(self):
        return f"<Order {self.id}>"
