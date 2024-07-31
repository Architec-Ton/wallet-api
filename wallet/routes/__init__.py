from fastapi import APIRouter, Depends

from .bank import router as bank_router
from .transfer import router as transfer_router
from .auth import router as auth_router
from .game import router as game_router
from .wallet import router as wallet_router

from .admin import router as admin_router
from .app import router as app_router
from .transfer import router as transfer_router
from .transaction import router as transaction_router
from ..auth.auth import api_admin_key_auth

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(wallet_router, prefix="")
router.include_router(transaction_router)
router.include_router(transfer_router, prefix="/transfer")
router.include_router(app_router, prefix="")
router.include_router(bank_router, prefix="")
router.include_router(game_router, prefix="/game")

router.include_router(
    admin_router, prefix="/admin", dependencies=[Depends(api_admin_key_auth)]
)
