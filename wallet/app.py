from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import logging
import time

from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from wallet.config import TORTOISE_ORM
from wallet.errors import APIException
from wallet.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)03d %(levelname)s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
)

app_base = "/api/v2/wallet"


app = FastAPI(
    title=f"Architec.TON API",
    debug=True,
    docs_url=f"{app_base}/docs",
    redoc_url=None,
    version="0.2.0",
    openapi_url=f"{app_base}/architecton.json",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.error},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


app.include_router(router, prefix=app_base)

register_tortoise(
    app, generate_schemas=True, add_exception_handlers=True, config=TORTOISE_ORM
)

app.mount("/storage", StaticFiles(directory="./storage"), name="storage")
