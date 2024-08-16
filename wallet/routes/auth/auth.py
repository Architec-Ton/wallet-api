import asyncio
import logging
import uuid

from fastapi import APIRouter
from tonsdk.utils import Address

from wallet.auth.token import create_token
from wallet.config import TON_CLIENT_NETWORK
from wallet.controllers.account_controller import AccountController
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

    async def bg_update_account(init_data):
        account = await AccountController.get_or_create(init_data)
        if init_data.init_ton and init_data.init_ton.address:
            wallet = await WalletController.get_or_create(Address(init_data.init_ton.address))
            if wallet and account:
                _ = await AccountController.get_or_create_wallet_connection(account, wallet)
                _ = await WalletController.update_from_network(wallet)
        logging.info(f"Account: {account}")

    if init_data.init_ton:
        payload["address"] = init_data.init_ton.address
        payload["net"] = TON_CLIENT_NETWORK

    if init_data.init_data_raw:
        payload["name"] = init_data.init_data_raw.user.username
        payload["lang"] = init_data.init_data_raw.user.language_code
        payload["sub"] = str(init_data.init_data_raw.user.id)

    access_token = create_token(payload)
    # s = telegram_validate(init_data)
    # logging.info(f"Validate: \n{s}")

    asyncio.ensure_future(bg_update_account(init_data))

    return AuthOut(access_token=access_token)
