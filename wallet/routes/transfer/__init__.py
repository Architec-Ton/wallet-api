from fastapi import APIRouter

from .send import router as send_router

router = APIRouter(tags=["Transfer"])  # , dependencies=[Depends(get_user)])

router.include_router(send_router, prefix="/send")
