from fastapi import APIRouter

order_router = APIRouter(tags=["order"])


@order_router.get("/")
async def home():
    return {"health": "ok"}
