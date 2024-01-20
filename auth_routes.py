from fastapi import APIRouter, HTTPException, status
from werkzeug.security import generate_password_hash, check_password_hash
from database import Session, engine
from schemas import SignUpModel
from models import User

auth_router = APIRouter(tags=["auth"])

session = Session(bind=engine)


@auth_router.get("/")
async def health():
    return {"health": "ok"}


@auth_router.post("/signup", response_model=SignUpModel, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_user = bool(session.query(User).filter((User.username == user.username) | (User.email == user.email)).first())
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exists")
    new_user = User(
        username=user.email,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )
    session.add(new_user)
    session.commit()
    return new_user
