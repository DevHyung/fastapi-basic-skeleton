from fastapi import APIRouter
from api.routes import v1_login

api_router = APIRouter()

api_router.include_router(v1_login.router, tags=["LOGIN"])
