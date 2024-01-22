from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from async_fastapi_jwt_auth import AuthJWT
from jwt_bearer import JWTBearer
from models import User, Order
from schemas import OrderModel, OrderStatusModel
from database import SessionLocal, engine

order_router = APIRouter(tags=["orders"])

session = SessionLocal(bind=engine)


@order_router.get("/hello")
async def hello():
    return {"hello": "world!"}


@order_router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
async def place_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    """
        ### Represents the HTTP POST request for /orders endpoint.

    - **order**: The JSON request object with Pizza_Size, Quantity.
    - **query_param**: No Query Params.

    ### Returns:
      - JSON object with the order information.
    """
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
        "order_by": new_order.user.username,
    }
    return jsonable_encoder(response)


@order_router.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def list_all_orders(Authorize=Depends(JWTBearer())):
    """
        ### Represents the HTTP GET request for /orders endpoint.

    - **query_param**: No Query Params.

    ### Returns:
      - List of JSON object with the order information.
    """

    username = await Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == username).first()
    if db_user.is_staff:
        orders = session.query(Order).all()
        return jsonable_encoder(orders)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid superuser")


@order_router.get("/{id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def get_order_by_id(id: int, Authorize=Depends(JWTBearer())):
    """
        ### Represents the HTTP GET request for /orders/{id} endpoint.

    - **query_param**: id of the order.

    ### Returns:
      - JSON object with the order information.
    """
    username = await Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == username).first()
    if db_user.is_staff:
        order = session.query(Order).filter(Order.id == id).first()
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
        return jsonable_encoder(order)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid superuser")


@order_router.get("/user/orders", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def get_all_order_by_user_id(Authorize=Depends(JWTBearer())):
    """
        ### Represents the HTTP GET request for /orders/user/orders endpoint.

    - **query_param**: No Query Params.

    ### Returns:
      - List of JSON object with all the order information of a user.
    """
    username = await Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == username).first()
    return jsonable_encoder(db_user.orders)


@order_router.get("/user/orders/{order_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def get_order_by_order_id(id: int, Authorize=Depends(JWTBearer())):
    """
        ### Represents the HTTP GET request for /orders/user/orders/{order_id} endpoint.

    - **query_param**: id of the order.

    ### Returns:
      - JSON object with the order information of the user by order id.
    """
    username = await Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == username).first()
    if db_user.is_staff:
        order = session.query(Order).filter(Order.id == id).first()
    else:
        order = session.query(Order).filter(Order.user_id == db_user.id, Order.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")

    return jsonable_encoder(order)


@order_router.put("/order/{order_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def update_order_by_order_id(id: int, order: OrderModel, Authorize=Depends(JWTBearer())):
    """
        ### Represents the HTTP PUT request for /orders/{order_id}/ endpoint.

    - **order**: The JSON request object with pizza_size, quantity.
    - **query_param**: id of the order.

    ### Returns:
      - JSON object with the updated order information.
    """
    username = await Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == username).first()
    db_order = session.query(Order).filter(Order.user_id == db_user.id, Order.id == id).first()
    db_order.quantity = order.quantity
    db_order.pizza_size = order.pizza_size
    session.commit()
    response = {
        "id": db_order.id,
        "pizza_size": db_order.pizza_size,
        "quantity": db_order.quantity,
        "order_status": db_order.order_status,
        "order_by": db_order.user.username,
    }
    return jsonable_encoder(response)


@order_router.put("/order/status/{order_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def update_order_status_by_order_id(id: int, order: OrderStatusModel, Authorize=Depends(JWTBearer())):
    """
        ### Represents the HTTP PUT request for /orders/order/status/{order_id} endpoint.

    - **order**: The JSON request object with order_status.
    - **query_param**: id of the order.

    ### Returns:
      - JSON object with the updated order information.
    """
    username = await Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == username).first()
    if not db_user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user must be admin")
    db_order = session.query(Order).filter(Order.id == id).first()
    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    db_order.order_status = order.order_status
    session.commit()
    response = {
        "id": db_order.id,
        "pizza_size": db_order.pizza_size,
        "quantity": db_order.quantity,
        "order_status": db_order.order_status,
        "order_by": db_order.user.username,
    }
    return jsonable_encoder(response)


@order_router.delete("/order/{order_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer())])
async def delete_order_by_order_id(id: int, Authorize=Depends(JWTBearer())):
    """
        ### Represents the HTTP DELETE request for /orders/order/{id} endpoint.

    - **query_param**: id of the order.

    ### Returns:
      - No Content
    """
    username = await Authorize.get_jwt_subject()
    db_user = session.query(User).filter(User.username == username).first()
    if not db_user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user must be admin")
    db_order = session.query(Order).filter(Order.id == id).first()
    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    session.delete(db_order)
    session.commit()
