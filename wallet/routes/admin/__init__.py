from fastapi import APIRouter
from .jetton import router as jetton_router
from .category import router as category_router
from .app import router as app_router
from .attachment import router as attachment_router
from .marketing import router as marketing_router


router = APIRouter(tags=["Admin"])

router.include_router(jetton_router, prefix="/jetton")
router.include_router(category_router, prefix="/categor")
router.include_router(app_router, prefix="/app")
router.include_router(marketing_router, prefix="/marketing")
router.include_router(attachment_router, prefix="/attachment")
