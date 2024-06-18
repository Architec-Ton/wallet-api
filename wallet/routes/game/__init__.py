from fastapi import APIRouter
from .games import router as games_router
from .game import router as game_router


router = APIRouter(tags=["Games"])

router.include_router(games_router)
router.include_router(game_router)
