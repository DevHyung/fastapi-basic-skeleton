from time import perf_counter

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from contextlib import asynccontextmanager
import uvicorn

from api.v1 import api_router

from core.config import CONFIG

from core.log import logger, access_logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.name}"
    #return f"{route.tags[0]}-{route.name}"


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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = perf_counter()
    client_ip = request.client.host
    client_port = request.client.port
    method = request.method
    url = request.url.path
    query_params = dict(request.query_params)
    path_params = request.path_params
    body = await request.body()

    response = await call_next(request)
    elapsed = round(perf_counter() - start_time, 4)
    status_code = response.status_code
    access_logger.info(
        f'status {status_code} | {elapsed}s | {client_ip}:{client_port} - "{method} {url}"\n'
        f'Query Params: {query_params}\n'
        f'Path Params: {path_params}\n'
        f'Body: {body.decode("utf-8") if body else None}'
    )
    return response


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
