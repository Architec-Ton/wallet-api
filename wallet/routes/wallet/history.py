from typing import List

from fastapi import APIRouter, Depends
from tonsdk.utils import Address

from wallet.auth import get_user
from wallet.controllers.transaction_controller import TransactionController
from wallet.view.auth.user import UserOut
from wallet.view.transaction.history import HistoryItemOut

router = APIRouter()


@router.get("", response_model=List[HistoryItemOut])
async def get_wallet_history(
    user: UserOut = Depends(get_user),
):
    # address = "EQAeirps_xb3Pl7jd43T_LzXH2k35FC6eQApOvFAOe0Emad3"
    address = user.address
    if address:
        return await TransactionController().get_trx(Address(address), limit=10)
    # return await TonController().get_transactions(Address(user.address), limit=25)
