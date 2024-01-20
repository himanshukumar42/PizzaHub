from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router

app = FastAPI()


@app.get("/", tags=["main"])
def health():
    return {"health": "ok"}


app.include_router(auth_router, prefix="/auth")
app.include_router(order_router, prefix="/order")
