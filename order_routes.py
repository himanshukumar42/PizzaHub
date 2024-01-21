from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from async_fastapi_jwt_auth import AuthJWT
from jwt_bearer import JWTBearer
from models import User, Order
from schemas import OrderModel
from database import SessionLocal, engine

order_router = APIRouter(tags=["orders"])

session = SessionLocal(bind=engine)


@order_router.get("/", dependencies=[Depends(JWTBearer())])
async def home():
    return {"health": "ok"}


@order_router.post("/order", status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
async def post_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    username = await Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == username).first()
    new_order = Order(
        quantity=order.quantity,
        pizza_size=order.pizza_size,
        user_id=db_user.id
    )
    session.add(new_order)
    session.commit()
    response = {
        "id": new_order.id,
        "pizza_size": new_order.pizza_size.value,
        "quantity": new_order.quantity,
        "order_status": new_order.order_status.value,
        "order_by": db_user.username,
    }
    return jsonable_encoder(response)
