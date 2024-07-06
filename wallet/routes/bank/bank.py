import asyncio
import logging
import random
import uuid
from typing import List
from faker import Faker
from tonsdk.utils import Address

from wallet.auth import get_user
from wallet.controllers.wallet_controller import WalletController
from wallet.view.auth.user import UserOut
from wallet.view.bank.BankBuyInfo import BankBuyInfo
from wallet.view.game.game import GameOut

fake = Faker()

from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/buy")  # , response_model=BankBuyInfo)
async def get_bank_assets(
    user: UserOut = Depends(get_user),
):
    owner_address = Address(user.address)
    # owner_address = Address("0QCto-hxbOIBe_G6ub3s3_murlWrPBo__j8zI4Fka8PAMGBK")

    ton, bnk = await asyncio.gather(
        WalletController().get_assets(
            owner_address, only_active=True, include_symbols=["TON"]
        ),
        WalletController().get_assets(
            owner_address, only_active=False, include_symbols=["BNK"]
        ),
    )

    logging.info(ton)
    logging.info(bnk)

    return {
        "ton": ton[0],
        "bnk": bnk[0],
        "contract": "kQBmyiov17J71ontt2u1F_dwKTfcUoghCMVyfIsDRM9NNvhp",
    }
