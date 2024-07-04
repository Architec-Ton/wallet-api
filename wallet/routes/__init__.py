from fastapi import APIRouter

from .auth import router as auth_router
from .game import router as game_router
from .wallet import router as wallet_router

from .admin import router as admin_router
from .app import router as app_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(wallet_router, prefix="")
router.include_router(app_router, prefix="")
router.include_router(game_router, prefix="/game")

router.include_router(admin_router, prefix="/admin")
