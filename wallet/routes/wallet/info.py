import random
import uuid
from typing import List
from faker import Faker

from wallet.view.wallet.info import InfoOut

fake = Faker()

from fastapi import APIRouter, Depends

router = APIRouter()

mock = [{"usd_price": 343.24, "address": "wefwefwfJHJKHewfwhejkfhjkhekS", "change_price": 0,

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
                     "description": "TON "
                 }
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
                     "description": "Tether Token for Tether USD"
                 }
             },

         ]
         }]


@router.get("", response_model=List[InfoOut])
async def get_wallet_info(
        # user: UserOut = Depends(get_user),
):
    return mock
