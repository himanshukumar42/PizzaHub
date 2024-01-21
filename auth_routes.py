from fastapi import APIRouter, HTTPException, status, Depends
from werkzeug.security import generate_password_hash, check_password_hash
from async_fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from datetime import timedelta
from database import SessionLocal, engine
from schemas import SignUpModel, LoginModel
from jwt_bearer import JWTBearer
from models import User

auth_router = APIRouter(tags=["auth"])

session = SessionLocal(bind=engine)


@auth_router.get("/", dependencies=[Depends(JWTBearer())])
async def health():
    return {"health": "ok"}


@auth_router.post("/signup", response_model=SignUpModel, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_user = bool(session.query(User).filter((User.username == user.username) | (User.email == user.email)).first())
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exists")
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )
    session.add(new_user)
    session.commit()
    return new_user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter((User.username == user.username)).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user does not exists")
    if not check_password_hash(db_user.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid password")

    access_token = await Authorize.create_access_token(
        subject=db_user.username,
        algorithm="HS256",
        user_claims={
            "user_id": db_user.id,
            "username": db_user.username,
            "is_staff": db_user.is_staff,
            "is_active": db_user.is_active,
        },
        expires_time=timedelta(minutes=10),
    )
    refresh_token = await Authorize.create_refresh_token(
        subject=db_user.username,
        algorithm="HS256",
        user_claims={
            "user_id": db_user.id,
            "username": db_user.username,
            "is_staff": db_user.is_staff,
            "is_active": db_user.is_active,
        },
        expires_time=timedelta(minutes=10),
    )
    response = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    return jsonable_encoder(response)


@auth_router.get("/refresh", status_code=status.HTTP_200_OK)
async def refresh(Authorize: AuthJWT = Depends()):
    username = await Authorize.get_jwt_subject()
    db_user = session.query(User).filter((User.username == username)).first()
    access_token = await Authorize.create_access_token(
        subject=db_user.username,
        algorithm="HS256",
        user_claims={
            "user_id": db_user.id,
            "username": db_user.username,
            "is_staff": db_user.is_staff,
            "is_active": db_user.is_active,
        },
        expires_time=timedelta(minutes=10),
    )
    refresh_token = await Authorize.create_refresh_token(
        subject=db_user.username,
        algorithm="HS256",
        user_claims={
            "user_id": db_user.id,
            "username": db_user.username,
            "is_staff": db_user.is_staff,
            "is_active": db_user.is_active,
        },
        expires_time=timedelta(minutes=10),
    )
    response = {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    return jsonable_encoder(response)
