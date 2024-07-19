from fastapi import APIRouter, Depends
from .info import router as info_router
from .assets import router as assets_router
from .history import router as history_router


router = APIRouter()

router.include_router(assets_router, prefix="/assets")
router.include_router(info_router, prefix="/info")
router.include_router(history_router, prefix="/history")
