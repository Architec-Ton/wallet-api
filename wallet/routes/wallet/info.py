import logging

from fastapi import APIRouter, Depends
from tonsdk.utils import Address

from wallet.auth import get_user
from wallet.controllers.transaction_controller import TransactionController
from wallet.controllers.wallet_controller import WalletController
from wallet.view.auth.user import UserOut
from wallet.view.wallet.info import InfoOut, WalletOut

router = APIRouter()


@router.get("", response_model=InfoOut)
async def get_wallet_info(
    user: UserOut = Depends(get_user),
):
    # logging.info(user)

    wc = WalletController()

    address = Address(user.address)
    seqno = None
    assets = []
    txs = []
    usd_price = 0
    try:
        # seqno = await wc.update_transaction(address)
        # address = Address("0QCto-hxbOIBe_G6ub3s3_murlWrPBo__j8zI4Fka8PAMGBK")
        # has_transaction = await wc.update_transaction(address)
        assets = await wc.get_assets(address)
        # txs = await TransactionController().get_transactions(address, limit=3)
        txs = await TransactionController().get_trx(Address(address), limit=3)
        # txs = await TonController().get_transactions(address)
        usd_price = sum([a.usd_price for a in assets if a.usd_price is not None])
    except BaseException as e:
        logging.error(e)

    # transactions = await TonController().get_transactions(Address(user.address))
    # logging.info(transactions)
    #
    # logging.info(f"Balance: {balance}")
    # for t in transactions:
    #     logging.info(f"transactions: {t.to_dict()}")

    change_price = 0.01

    wallet = WalletOut(
        address=address.to_string(is_user_friendly=True),
        usd_price=usd_price,
        change_price=change_price,
        assets=assets,
        history=txs,
        seqno=seqno,
    )

    return {"current_wallet": 0, "wallets": [wallet]}
