from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from async_fastapi_jwt_auth import AuthJWT
from jwt_bearer import JWTBearer
from models import User, Order
from schemas import OrderModel
from database import SessionLocal, engine

order_router = APIRouter(tags=["orders"])

session = SessionLocal(bind=engine)


@order_router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
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


@order_router.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def list_all_orders(Authorize=Depends(JWTBearer())):
    username = await Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == username).first()
    if db_user.is_staff:
        orders = session.query(Order).all()
        all_orders = [{
            "id": order.id,
            "pizza_size": order.pizza_size.value,
            "quantity": order.quantity,
            "order_status": order.order_status.value,
            "order_by": order.user_id
        } for order in orders]
        return jsonable_encoder(all_orders)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid superuser")


@order_router.get("/{id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def get_order_by_id(id: int, Authorize=Depends(JWTBearer())):
    username = await Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == username).first()
    if db_user.is_staff:
        order = session.query(Order).filter(Order.id == id).first()
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
        order_dict = {
            "id": order.id,
            "pizza_size": order.pizza_size.value,
            "quantity": order.quantity,
            "order_status": order.order_status.value,
            "order_by": order.user_id
        }
        return jsonable_encoder(order_dict)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid superuser")


@order_router.get("/user/orders", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def get_all_order_by_user_id(Authorize=Depends(JWTBearer())):
    username = await Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == username).first()
    return jsonable_encoder(db_user.orders)
    # if not db_user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    # order = session.query(Order).filter(Order.user_id == db_user.id).first()
    # if order is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    # order_dict = {
    #     "id": order.id,
    #     "pizza_size": order.pizza_size.value,
    #     "quantity": order.quantity,
    #     "order_status": order.order_status.value,
    #     "order_by": order.user_id
    # }
    # return jsonable_encoder(order_dict)
