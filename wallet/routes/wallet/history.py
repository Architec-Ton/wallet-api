import logging
import random
import uuid
from typing import List
from faker import Faker
from tonsdk.utils import Address

from wallet.auth import get_user
from wallet.controllers.ton_controller import TonController
from wallet.controllers.transaction_controller import TransactionController
from wallet.controllers.wallet_controller import WalletController
from wallet.models.base_transaction_model import BaseTransaction
from wallet.view.auth.user import UserOut
from wallet.view.transaction.history import HistoryItemOut
from wallet.view.wallet.info import InfoOut

fake = Faker()

from fastapi import APIRouter, Depends

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
