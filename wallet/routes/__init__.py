from fastapi import APIRouter

from .game import router as game_router

router = APIRouter()

router.include_router(game_router, prefix="/game")
