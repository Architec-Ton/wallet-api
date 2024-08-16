from fastapi import APIRouter

from .app import router as app_router

router = APIRouter(tags=["Apps"])  # , dependencies=[Depends(get_user)])

router.include_router(app_router, prefix="/app")
