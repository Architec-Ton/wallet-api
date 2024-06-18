from fastapi import APIRouter, Depends

from .game import router as game_router
from ..auth import get_user

router = APIRouter()

router.include_router(game_router, prefix="/game", dependencies=[Depends(get_user)])
