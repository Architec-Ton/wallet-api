from fastapi import APIRouter, Depends
from .games import router as games_router
from .game import router as game_router
from ...auth import get_user

router = APIRouter(tags=["Games"], dependencies=[Depends(get_user)])

router.include_router(games_router)
router.include_router(game_router)
