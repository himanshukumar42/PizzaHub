from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from auth_routes import auth_router
from order_routes import order_router
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from schemas import Settings

description = """
PizzaHub API helps you do awesome stuff. 🚀

## Orders

You can **read orders**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""
app = FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/", tags=["main"])
def health():
    return {"health": "ok"}


app.include_router(auth_router, prefix="/auth")
app.include_router(order_router, prefix="/orders")
