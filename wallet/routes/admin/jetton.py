import logging

from fastapi import APIRouter
from tonsdk.utils import Address

from wallet.config import TON_CLIENT_NETWORK
from wallet.controllers.ton_controller import TonController
from wallet.models import JettonMaster
from wallet.view.jetton.jetton import AdminAddJettonIn

router = APIRouter()


async def create_jetton_master(address: str):
    jetton, _ = await JettonMaster.get_or_create(address_base64=address)
    jetton.address = address
    jetton.mainnet = False  # Dev only for testnet
    await jetton.save()
    return jetton


@router.post("/create")
async def post_create_jettons(
    jetton_in: AdminAddJettonIn
):
    jt = await create_jetton_master(jetton_in.address)
    jetton_data = await TonController().get_jetton_data(Address(jetton_in.address))
    jt.decimals = jetton_data.decimals
    jt.symbol = jetton_data.symbol
    jt.name = jetton_data.name
    jt.description = jetton_data.description
    jt.supply = jetton_data.supply
    jt.token_supply = jetton_data.token_supply
    jt.image = jetton_data.image
    jt.address_base64 = jetton_data.address
    await jt.save()

    return jt


@router.post("/import")
async def post_imposrt_jettons():
    if TON_CLIENT_NETWORK == "testnet":
        jettons = [
            "kQBuFWV6jW_9F69A3qjn5rpqfG4eIMBJs9GFSrZU7d33EmIG",
            #  "kQCkaGQTCUMUzu5b9IDYY4EjGI4hLIrnnKa5oAhgymxp9pES",  # BNK
            "kQDJ4yZlYHbwbUtFAtyk7YOMt7cWUY-Hk0TB9-pg2ZOxHMMf",
            # "kQCidZd9oBoqDtTSp91BCTMvcpwGJkut7qdtOZKZXlVnBDb7",  # ARC
            "EQDnRHbK5vJBLQyAnS6V8XNoRerCebnn9A2FlVlHtFVLFGZ-",
        ]
    else:
        jettons = [
            "EQAj1qW6WZTd7sd33Uk48O3TqxNPMjYrgwRHAcBM8RcQCQAD",
            #  "kQCkaGQTCUMUzu5b9IDYY4EjGI4hLIrnnKa5oAhgymxp9pES",  # BNK
            "EQBXRdZTk5P49mL0nOYfDR1VR33N3sPUgB7PNQMaj6DhxOJH",
            # "kQCidZd9oBoqDtTSp91BCTMvcpwGJkut7qdtOZKZXlVnBDb7",  # ARC
            "EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs",
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
