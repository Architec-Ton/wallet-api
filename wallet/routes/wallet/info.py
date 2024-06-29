import logging
import random
import uuid
from typing import List
from faker import Faker
from tonsdk.utils import Address

from wallet.auth import get_user
from wallet.controllers.ton_controller import TonController
from wallet.view.auth.user import UserOut
from wallet.view.wallet.info import InfoOut

fake = Faker()

from fastapi import APIRouter, Depends

router = APIRouter()

mock = [
    {
        "usd_price": 343.24,
        "address": "wefwefwfJHJKHewfwhejkfhjkhekS",
        "change_price": 0,
        "assets": [
            {
                "amount": 5,
                "usd_price": 5 * 7.4300000000233244,
                "change_price": 0.112,
                "type": "ton",
                "meta": {
                    "name": "TON",
                    "symbol": "TON",
                    "decimals": "9",
                    "image": "https://cache.tonapi.io/imgproxy/T3PB4s7oprNVaJkwqbGg54nexKE0zzKhcrPv8jcWYzU/rs:fill:200:200:1/g:no/aHR0cHM6Ly90ZXRoZXIudG8vaW1hZ2VzL2xvZ29DaXJjbGUucG5n.webp",
                    "description": "TON ",
                },
            },
            {
                "amount": 5,
                "usd_price": 5 * 1.0123213222,
                "change_price": 0.012,
                "type": "jetton",
                "meta": {
                    "address": "0:b113a994b5024a16719f69139328eb759596c38a25f59028b146fecdc3621dfe",
                    "name": "Tether USD",
                    "symbol": "USD₮",
                    "decimals": "6",
                    "image": "https://cache.tonapi.io/imgproxy/T3PB4s7oprNVaJkwqbGg54nexKE0zzKhcrPv8jcWYzU/rs:fill:200:200:1/g:no/aHR0cHM6Ly90ZXRoZXIudG8vaW1hZ2VzL2xvZ29DaXJjbGUucG5n.webp",
                    "description": "Tether Token for Tether USD",
                },
            },
            {
                "amount": 135,
                "usd_price": 135 * 1.5 * 7.545,
                "change_price": -0.512,
                "type": "jetton",
                "meta": {
                    "address": "0:b113a994b5024a16719f69139328eb759596c38a25f59028b146fecdc3621dfe",
                    "name": "Architec.Ton Banks",
                    "symbol": "BNK",
                    "decimals": "6",
                    "image": "https://cache.tonapi.io/imgproxy/4KCMNm34jZLXt0rqeFm4rH-BK4FoK76EVX9r0cCIGDg/rs:fill:200:200:1/g:no/aHR0cHM6Ly9jZG4uam9pbmNvbW11bml0eS54eXovY2xpY2tlci9ub3RfbG9nby5wbmc.webp",
                    "description": "Tether Token for Tether USD",
                },
            },
        ],
    }
]


@router.get("", response_model=InfoOut)
async def get_wallet_info(
    user: UserOut = Depends(get_user),
):
    logging.info(user)

    balance = await TonController().get_balance(Address(user.address))

    transactions = await TonController().get_transactions(Address(user.address))

    logging.info(f"Balance: {balance}")
    for t in transactions:
        logging.info(f"transactions: {t.to_dict()}")

    mock[0]["address"] = user.address
    mock[0]["assets"][0]["amount"] = balance
    mock[0]["assets"][0]["usd_price"] = balance * 7.02323

    mock[0]["usd_price"] = mock[0]["assets"][0]["usd_price"]
    return {"current_wallet": 0, "wallets": mock}
