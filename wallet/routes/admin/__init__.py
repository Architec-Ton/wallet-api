from fastapi import APIRouter
from .jetton import router as jetton_router


router = APIRouter(tags=["Admin"])

router.include_router(jetton_router, prefix="/jetton")
