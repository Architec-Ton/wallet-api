from fastapi import APIRouter

from .bank import router as bank_router

router = APIRouter(tags=["Bank"])  # , dependencies=[Depends(get_user)])

router.include_router(bank_router, prefix="/bank")
