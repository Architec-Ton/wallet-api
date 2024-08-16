from fastapi import APIRouter

from .transaction import router as transaction_router

router = APIRouter(tags=["Transaction"])  # , dependencies=[Depends(get_user)])

router.include_router(transaction_router, prefix="/transaction")
