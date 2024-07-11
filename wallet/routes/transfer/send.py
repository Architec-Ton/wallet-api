import asyncio
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

from fastapi import APIRouter, Depends, Query

router = APIRouter()


@router.get("")  # , response_model=BankBuyInfo)
async def get_send_info(
    send: str = Query(),
    recv: str = Query(),
    user: UserOut = Depends(get_user),
):
    owner_address = Address(user.address)
    # owner_address = Address("0QCto-hxbOIBe_G6ub3s3_murlWrPBo__j8zI4Fka8PAMGBK")

    send, recv = await asyncio.gather(
        WalletController().get_assets(
            owner_address, only_active=True, include_symbols=[send.upper().strip()]
        ),
        WalletController().get_assets(
            owner_address, only_active=False, include_symbols=[recv.upper().strip()]
        ),
    )

    return {"send": send, "recv": recv}