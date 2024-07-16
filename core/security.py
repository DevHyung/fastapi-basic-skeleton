from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import HTTPBearer

from core.config import CONFIG

from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer(scheme_name="CaREDIT Authorizetion", description="ACCESS-TOKEN")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="401: 인증실패",
    headers={"WWW-Authenticate": "Bearer"},
)


class IPWhitelistMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, allowed_ips: list):
        super().__init__(app)
        self.allowed_ips = allowed_ips

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        if client_ip not in self.allowed_ips:
            return Response(
                status_code=403,
                content='{"detail": "Forbidden"}',
                media_type='application/json'
            )
        return await call_next(request)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, CONFIG.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_token(token: HTTPBearer) -> str | None:
    try:
        bearer = token.credentials
        payload = jwt.decode(bearer, CONFIG.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except InvalidTokenError:
        return None

