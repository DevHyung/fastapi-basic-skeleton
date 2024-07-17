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

from model.request import ReqModelLogin
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

router = APIRouter(prefix="/user")


""" ========================= user-defined function """
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
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="401: JWT 존재하지않는 sub",
            headers={"WWW-Authenticate": "Bearer"},  # 401일땐 반환해줘야함
        )

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


""" ========================= router """
@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/bearer/check")
async def bearer_check(token=Depends(oauth2_scheme)):
    user_name = verify_token(token)
    if user_name is None:  # status 403
        raise credentials_exception

    # status 200
    return {
        "detail": f"Verify Bearer {user_name}"
    }


@router.post("/login", response_model=Token)
async def login(response: Response, req_login: ReqModelLogin):
    user: User = authenticate_user(GLOBALS.USERS_DB, req_login.email, req_login.password)
    if not user:  # status 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="401: 유효하지 않은 아이디 or 패스워드",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # status 200
    access_token_expires = timedelta(minutes=CONFIG.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,  # 토큰 주체 식별, 보통 ID
            'user_email' : user.email
        },
        expires_delta= access_token_expires
    )
    response.headers["Authorization"] = f"Bearer {access_token.strip()}"

    return Token(token_type="bearer",
                 access_token=access_token,
                 expire_datetime=(datetime.now() + access_token_expires).strftime("%Y-%m-%d %H:%M:%S"))