from typing import List

from fastapi import APIRouter, Depends
from tonsdk.utils import Address

from wallet.auth import get_user
from wallet.controllers.wallet_controller import WalletController
from wallet.view.auth.user import UserOut
from wallet.view.wallet.coin import CoinOut

router = APIRouter()


@router.get("", response_model=List[CoinOut])
async def get_wallet_assets(
    user: UserOut = Depends(get_user),
):
    owner_address = Address(user.address)
    # owner_address = Address("0QCto-hxbOIBe_G6ub3s3_murlWrPBo__j8zI4Fka8PAMGBK")

    return await WalletController().get_assets(owner_address)
