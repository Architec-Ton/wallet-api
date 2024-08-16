from typing import List

from fastapi import APIRouter, Depends, Query
from tonsdk.utils import Address

from wallet.auth import get_user
from wallet.controllers.ton_controller import TonController
from wallet.view.auth.user import UserOut
from wallet.view.transaction.history import HistoryItemOut

router = APIRouter()


@router.get("", response_model=List[HistoryItemOut])
async def get_send_info(
    send: str = Query(),
    recv: str = Query(),
    user: UserOut = Depends(get_user),
):
    owner_address = Address(user.address)
    # owner_address = Address("0QCto-hxbOIBe_G6ub3s3_murlWrPBo__j8zI4Fka8PAMGBK")

    # send, recv = await asyncio.gather(
    #     WalletController().get_assets(
    #         owner_address, only_active=True, include_symbols=[send.upper().strip()]
    #     ),
    #     WalletController().get_assets(
    #         owner_address, only_active=False, include_symbols=[recv.upper().strip()]
    #     ),
    # )

    # return {"send": send, "recv": recv}

    txs = await TonController().get_transactions(owner_address)

    # return [t.to_dict() for t in txs]

    # async with aiohttp.ClientSession() as session:
    #     url = "https://testnet.toncenter.com/api/v2/" + "getTransactions"
    #     transactions = []
    #     params = {"address": owner_address.to_string(), "limit": 10, "archival": 1}
    #     response = await session.get(url=url, params=params)
    #
    #     return await response.json()

    return txs
