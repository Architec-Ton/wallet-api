import logging

from fastapi import APIRouter, Depends
from tonsdk.utils import Address

from wallet.auth import get_user
from wallet.controllers.transaction_controller import TransactionController
from wallet.controllers.wallet_controller import WalletController
from wallet.view.auth.user import UserOut
from wallet.view.transaction.transaction import (
    TransactionItemCreateIn,
    TransactionItemCreateOut,
    TransactionItemOut,
    ton_icon,
)

router = APIRouter()


@router.get("s")  # , response_model=HistoryItemOut)
async def get_transaction(
    user: UserOut = Depends(get_user),
):
    address = user.address  # "EQB1VVAKYHxXrg-zlLH0V3xRuhobNrPOZUHz24ghzUDhZsNL"

    return await TransactionController().get_transactions(Address(address))


@router.post("")  # , response_model=HistoryItemOut)
async def create_outcoming_transaction(
    trx_in: TransactionItemCreateIn,
    user: UserOut = Depends(get_user),
):
    address = user.address  # "EQB1VVAKYHxXrg-zlLH0V3xRuhobNrPOZUHz24ghzUDhZsNL"

    transactions = await TransactionController().get_transactions(Address(address), limit=1)

    if len(transactions) > 0:
        lt = transactions[0]["utime"]
    else:
        lt = 0
    # lt = await TransactionController().get_outcoming_last_lt(Address(address))
    trx_id = None
    if lt is not None:
        lt = int(lt)  # + 1
        trx_id = f"{trx_in.destination}.{lt}".encode().hex()
    return TransactionItemCreateOut(destination=trx_in.destination, lt=lt, trx_id=trx_id)


@router.get("/{trx}")  # , response_model=TransactionItemOut)
async def get_outcoming_transaction(
    trx: str,
    user: UserOut = Depends(get_user),
):
    # address = "EQB1VVAKYHxXrg-zlLH0V3xRuhobNrPOZUHz24ghzUDhZsNL"
    address = user.address
    trx = None
    try:
        trx_id = bytes.fromhex(trx)
        destination, lt = trx_id.decode().split(".")

        trx = await TransactionController().get_outcomig_trx(Address(address), Address(destination), int(lt))
    except Exception as e:
        logging.error(e)

    # return trx

    usd_rate = 5.98
    comment = None

    if trx and trx["out_msgs"][0]["@type"] == "raw.message" and "message" in trx["out_msgs"][0]:
        comment = trx["out_msgs"][0]["message"]

    if trx is not None and len(trx["out_msgs"]) > 0:
        trx_out = TransactionItemOut(
            commission_amount=int(trx["fee"]) / 10**9,
            commission_usd=usd_rate * int(trx["fee"]) / 10**9,
            utime=int(trx["utime"]),
            amount=int(trx["out_msgs"][0]["value"]) / 10**9,
            amountUsd=usd_rate * int(trx["out_msgs"][0]["value"]) / 10**9,
            symbol="TON",
            comment=comment,
            icon_src=f"data:image/svg+xml;base64,{ton_icon}",
            source=address,
            destination=destination,
            status=False,
        )

        return trx_out


@router.get("s/seqno")  # , response_model=TransactionItemOut)
async def get_seqno(
    trx: str,
    user: UserOut = Depends(get_user),
):
    address = user.address  # "EQB1VVAKYHxXrg-zlLH0V3xRuhobNrPOZUHz24ghzUDhZsNL"

    return await WalletController().get_seqno(Address(address))
