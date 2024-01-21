from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPBase, HTTPBearerModel
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_403_FORBIDDEN
from schemas import Settings
from typing import Optional
import time
import jwt
from fastapi.security import HTTPAuthorizationCredentials


def decode_jwt(token: str):
    try:
        decode_token = jwt.decode(token, Settings().authjwt_secret_key, algorithms=Settings().authjwt_algorithm)
        return decode_token if decode_token["exp"] >= time.time() else None
    except Exception as e:
        print(str(e))
        return False


def verify_jwt(jwt_token: str) -> bool:
    is_token_valid: bool = False
    payload = decode_jwt(jwt_token)
    if payload:
        is_token_valid = True
    return is_token_valid


class AuthJWTBearer(HTTPBase):
    def __init__(self, *, scheme: str, bearerFormat: Optional[str] = None, scheme_name: Optional[str] = None,
                 description: Optional[str] = None, auto_error: bool = True):
        super().__init__(scheme=scheme, scheme_name=scheme_name, description=description, auto_error=auto_error)
        self.model = HTTPBearerModel(bearerFormat=bearerFormat, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(
            self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Invalid authentication credentials",
                )
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


class JWTBearer(AuthJWTBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error, scheme="Bearer ")

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request=request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid or expired token")
            if verify_jwt(credentials.credentials):
                return credentials.credentials
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid or expired token")
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid or expired token ")
