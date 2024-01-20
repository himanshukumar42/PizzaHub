from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from auth_routes import auth_router
from order_routes import order_router
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi_jwt_auth import AuthJWT
from schemas import Settings

app = FastAPI()


@app.exception_handlers(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=400,
        content={"detail": exc}
    )


@AuthJWT.load_config
def get_config():
    return Settings()


@app.get("/", tags=["main"])
def health():
    return {"health": "ok"}


app.include_router(auth_router, prefix="/auth")
app.include_router(order_router, prefix="/order")
