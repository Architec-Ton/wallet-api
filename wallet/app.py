from fastapi import FastAPI
from routes import router

app_base = "/api/v2"

app = FastAPI(
    title=f"Architec.TON API",
    debug=True,
    docs_url=f"{app_base}/docs",
    redoc_url=None,
    version="0.2.0",
    openapi_url=f"{app_base}/architecton.json",
)

app.include_router(router, prefix=app_base)
