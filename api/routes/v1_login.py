from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    status,
    Response
)
from fastapi.security import HTTPBearer
from model.user import (
    User,
    Token
)

from model.request import ReqLogin
from core.security import (
    verify_password,
    verify_token,
    create_access_token,
    oauth2_scheme,
    credentials_exception
)
from core.config import CONFIG
import core.globals as GLOBALS

from datetime import datetime, timedelta

router = APIRouter(prefix="/api")


def get_user(db, username: str) -> User | None:
    if username in db:
        user_dict = db[username]
        return User(**user_dict)
    return None


def authenticate_user(user_db, username: str, password: str):
    user = get_user(user_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


#async def get_current_user(token: str = Depends(oauth2_scheme)): # OAuth2PasswordBearer 의 경우
async def get_current_user(token: HTTPBearer = Depends(oauth2_scheme)):
    username = verify_token(token)
    if username is None:
        raise credentials_exception

    user = get_user(GLOBALS.USERS_DB, username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="401: 활성화되지 않은 유저",
            headers={"WWW-Authenticate": "Bearer"},  # 401일땐 반환해줘야함
        )
    return current_user


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/login")
#async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
async def login(response: Response, req_login: ReqLogin) -> Token:
    user: User = authenticate_user(GLOBALS.USERS_DB, req_login.email, req_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="401: 유효하지 않은 아이디 or 패스워드",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=CONFIG.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta= access_token_expires
    )
    response.headers["Authorization"] = f"Bearer {access_token.strip()}"

    return Token(access_token=access_token,
                 token_type="bearer",
                 expire_datetime=(datetime.now() + access_token_expires).strftime("%Y-%m-%d %H:%M:%S"))