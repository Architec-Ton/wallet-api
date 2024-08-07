import datetime
import logging
import random
import uuid
from typing import List
from faker import Faker

from fastapi import APIRouter
from tonsdk.utils import Address

from wallet.auth.auth import telegram_validate
from wallet.auth.token import create_token
from wallet.controllers.wallet_controller import WalletController
from wallet.view.auth.auth import AuthIn, AuthOut

router = APIRouter(tags=["Auth"])


@router.post("", response_model=AuthOut)
async def post_auth(init_data: AuthIn):

    # TODO: Check hash
    # TODO: Check signature
    logging.info(init_data)

    payload = {
        "iss": uuid.uuid4().hex,
    }

    if init_data.init_ton:
        payload["address"] = init_data.init_ton.address
        payload["net"] = "mainnet"

    if init_data.init_data_raw:
        payload["name"] = init_data.init_data_raw.user.username
        payload["lang"] = init_data.init_data_raw.user.language_code
        payload["sub"] = str(init_data.init_data_raw.user.id)

    access_token = create_token(payload)
    # s = telegram_validate(init_data)
    # logging.info(f"Validate: \n{s}")

    return AuthOut(access_token=access_token)
