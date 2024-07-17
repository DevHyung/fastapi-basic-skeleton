from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from contextlib import asynccontextmanager
import uvicorn

from api.v1 import api_router

from core.config import CONFIG

@asynccontextmanager
async def lifespan(app: FastAPI):
    pass
    yield


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


""" app 오브젝트 + Config """
app = FastAPI(title="TITLE_EXAMPLE",
              version="v0.0.1",
              docs_url="/api/docs",
              redoc_url="/api/redocs",
              openapi_url="/api/openapi.json",
              description="DESCRIPTION_EXAMPLE",
              lifespan=lifespan,
              generate_unique_id_function=custom_generate_unique_id)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 출처 목록
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메서드
    allow_headers=["*"],  # 허용할 HTTP 헤더
)
#app.add_middleware(security.IPWhitelistMiddleware, allowed_ips=GLOBALS.ALLOWED_IPS)

if __name__ == '__main__':
    """ 참조 https://github.com/tiangolo/full-stack-fastapi-template/tree/master/backend """
    MODE = CONFIG.TYPE
    # FOR DEBUG
    if MODE == "DEV":
        uvicorn.run(app="main:app",  # YOUR_FILE:YOUR_APP_OBJECT
                    host="0.0.0.0",  # INPUT_YOUR_HOST
                    port=50202,  # INPUT_YOUR_PORT
                    reload=True)  # IF_DEV_True
    elif MODE == "PROD":
        uvicorn.run(app="main:app",
                    host="0.0.0.0",
                    port=10203,
                    reload=False)
