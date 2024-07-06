import logging
import random
import uuid
from typing import List
from faker import Faker
from tonsdk.utils import Address

from wallet.auth import get_user
from wallet.controllers.ton_controller import TonController
from wallet.controllers.wallet_controller import WalletController
from wallet.models import JettonMaster
from wallet.view.auth.user import UserOut
from wallet.view.wallet.info import InfoOut

fake = Faker()

from fastapi import APIRouter, Depends

router = APIRouter()


async def create_jetton_master(address: str):
    jetton, _ = await JettonMaster.get_or_create(address_base64=address)
    jetton.address = address
    jetton.mainnet = False  # Dev only for testnet
    await jetton.save()
    return jetton


# EQBkmVvLkyZYouoNFnhf4622BoPoMw2mmEwyFIgxWviQuqke


# kQBmyiov17J71ontt2u1F_dwKTfcUoghCMVyfIsDRM9NNvhp CSv3
@router.post("/import")
async def post_imposrt_jettons():
    jettons = [
        "kQDDm3AwW9NAP2sv3ZjKPje9hY5zEiM68GxoUVtMX616n6Cm",  # BNK
        "kQA-NCq-ifSX0ytcNNB7mla5eLyLntZieRuRcJC-npnWWGFq",  # ARC
        "EQDnRHbK5vJBLQyAnS6V8XNoRerCebnn9A2FlVlHtFVLFGZ-",
    ]
    out = []
    for j in jettons:
        try:
            jt = await create_jetton_master(j)
            jetton_data = await TonController().get_jetton_data(Address(j))

            jt.decimals = jetton_data.decimals
            jt.symbol = jetton_data.symbol
            jt.name = jetton_data.name
            jt.description = jetton_data.description
            jt.supply = jetton_data.supply
            jt.token_supply = jetton_data.token_supply
            jt.image = jetton_data.image
            jt.address_base64 = jetton_data.address
            await jt.save()

            out.append(jetton_data.to_dict())
        except BaseException as e:
            logging.exception(e)

    return out
