import random
import uuid
from typing import List
from faker import Faker

from fastapi import APIRouter

from wallet.auth.token import create_token
from wallet.view.auth.auth import AuthIn, AuthOut

router = APIRouter(tags=["Auth"])


@router.post("", response_model=AuthOut)
async def post_auth(init_data: AuthIn):

    # TODO: Check hash
    # TODO: Check signature

    payload = {
        "name": "John Dou",
        "lang": (
            init_data.init_data_raw.user.language_code
            if init_data.init_data_raw
            else "en-En"
        ),
        "address": init_data.init_ton.address if init_data.init_ton else "sample",
        "net": "ton",
        "iss": uuid.uuid4().hex,
        "sub": (
            f"{init_data.init_data_raw.user.id}" if init_data.init_data_raw else "123"
        ),
    }
    access_token = create_token(payload)
    return AuthOut(access_token=access_token)
