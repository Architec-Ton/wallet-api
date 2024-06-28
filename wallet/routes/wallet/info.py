import random
import uuid
from typing import List
from faker import Faker

from wallet.auth import get_user
from wallet.view.auth.user import UserOut
from wallet.view.game.game import GameOut

fake = Faker()

from fastapi import APIRouter, Depends

router = APIRouter()

mock = {"balance": {"amount": 54545.545, "currency": "USD"}}


@router.get("")
async def get_wallet_info(
    # user: UserOut = Depends(get_user),
):

    return mock
